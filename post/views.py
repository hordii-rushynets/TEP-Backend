from django.db.models import Q
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import CartItem
from post.services import LiqPayService
from post.services.abstract_delivery_service import AbstractDeliveryService, create_order
from tep_user.authentication import IgnoreInvalidTokenAuthentication
from tep_user.services import IPControlService, RedisDatabases

from .models import Order
from .serializers import OrderSerializer
from .services.factory import get_delivery_service


class CreateParcelView(APIView):
    authentication_classes = [IgnoreInvalidTokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, service_type):
        data = request.data.copy()
        cart_item_ids = request.data.get('cart_item_ids', [])
        product_variant_ids = []
        total_price = 0
        total_weight = 0
        total_title = []
        order_item_data = []

        for item_id in cart_item_ids:
            try:
                cart_item = CartItem.objects.get(id=item_id)
                product_variant = cart_item.product_variants
                product_variant_ids.append(product_variant.id)

                if product_variant.promotion:
                    price = product_variant.promo_price
                elif product_variant.is_wholesale:
                    price = product_variant.wholesale_price
                else:
                    price = product_variant.default_price

                total_price += price * cart_item.quantity
                total_weight += product_variant.weight * cart_item.quantity
                total_title.append(product_variant)

                order_item_data.append({
                    'product_variant_id': product_variant.id,
                    'color_id': cart_item.color.id if cart_item.color else None,
                    'material_id': cart_item.material.id if cart_item.material else None,
                    'size_id': cart_item.size.id if cart_item.size else None,
                    'filter_field_ids': list(cart_item.filter_field.values_list('id', flat=True)),
                    'quantity': cart_item.quantity
                })

            except CartItem.DoesNotExist:
                continue

        data['cost'] = total_price
        data['weight'] = total_weight
        data['tep_user'] = request.user if request.user.is_authenticated else None
        data['ip_address'] = IPControlService(request, RedisDatabases.IP_CONTROL).get_ip()
        data['description'] = ', '.join([str(product_variant.title) for product_variant in total_title])
        data['order_item_data'] = order_item_data

        order = create_order(
            tep_user=data.get('tep_user'),
            ip_address=data.get('ip_address'),
            post_type=service_type,
            order_item_data=data.get('order_item_data', []),
            price=total_price,
            weight=total_weight,
            payment_method=request.data.get('payment_method')
        )

        service: AbstractDeliveryService = get_delivery_service(service_type)

        if request.data.get('payment_method') == Order.BY_CARD:
            return self._redirect_to_pay_online(request, service, data, order.id, total_price, request.get_host())

        parcel = service.create_parcel(data) 

        order.number = parcel.get('number')
        order.unique_post_code = parcel.get('post_code')

        return Response(parcel, status=status.HTTP_201_CREATED)

    def _redirect_to_pay_online(self, request: HttpRequest, service: AbstractDeliveryService, request_data: dict, order_id: int, total_price: float, request_host: str) -> HttpResponse:
        delivery_cost = service.calculate_delivery_cost(request_data)
        amount = total_price + delivery_cost.get('cost')

        liqpay_service: LiqPayService = LiqPayService()
        payment_template_data = liqpay_service.create_payment_template_data(amount, order_id, request_host, request_data)

        return render(request, 'pay.html', payment_template_data)


class VerifyPaymentView(APIView):
    authentication_classes = [IgnoreInvalidTokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        liqpay_service: LiqPayService = LiqPayService()
        payment_decoded_data = liqpay_service.verify_payment(request.data.get('signature'), request.data.get('data'))
        host = request.get_host()

        if payment_decoded_data:
            order = Order.objects.get(id=payment_decoded_data.get('order_id'))
            order.paid = True
            order.save()

            service: AbstractDeliveryService = get_delivery_service(order.post_type)
            parcel = service.create_parcel(payment_decoded_data)
            parcel_number = parcel.get("number")

            order.number = parcel_number
            order.save()
            return HttpResponseRedirect(f'https://{host}/purchase/confirmation?parcel_number={parcel_number}')

        return HttpResponseRedirect(f'https://{host}/account/cart')


class GetWarehousesView(APIView):
    authentication_classes = [IgnoreInvalidTokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, service_type):
        service: AbstractDeliveryService = get_delivery_service(service_type)
        response = service.get_warehouses(request.data)
        return Response(response, status=status.HTTP_200_OK)


class TrackParcelView(APIView):
    authentication_classes = [IgnoreInvalidTokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, tracking_number):
        try:
            order = Order.objects.get(number=tracking_number)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        service = get_delivery_service(order.post_type)
        response = service.track_parcel(tracking_number)
        return Response(response)


class CalculateDeliveryCostView(APIView):
    authentication_classes = [IgnoreInvalidTokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, service_type):
        service = get_delivery_service(service_type)
        data = request.data
        response = service.calculate_delivery_cost(data)
        return Response(response)


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ip_address = IPControlService(self.request, RedisDatabases.IP_CONTROL).get_ip()
        return Order.objects.filter(Q(tep_user=self.request.user) | Q(ip_address=ip_address))

