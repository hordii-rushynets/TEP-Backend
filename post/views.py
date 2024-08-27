from cart.models import CartItem
from tep_user.services import IPControlService, RedisDatabases

from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order
from .serializers import OrderSerializer
from .services.factory import get_delivery_service

from tep_user.authentication import IgnoreInvalidTokenAuthentication


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
                    'filter_field_id': cart_item.filter_field.id if cart_item.filter_field else None,
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

        service = get_delivery_service(service_type)
        response = service.create_parcel(data)
        return Response(response, status=status.HTTP_201_CREATED)


class GetWarehousesView(APIView):
    authentication_classes = [IgnoreInvalidTokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, service_type):
        service = get_delivery_service(service_type)
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
        user = self.request.user
        return Order.objects.filter(tep_user=user)

