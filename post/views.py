from .services.factory import get_delivery_service
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from cart.models import CartItem
from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer


class CreateParcelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, service_type):
        data = request.data.copy()
        cart_item_ids = request.data.get('cart_item_ids', [])
        product_variant_ids = []
        total_price = 0
        total_weight = 0

        for item_id in cart_item_ids:
            try:
                cart_item = CartItem.objects.get(id=item_id)
                product_variant = cart_item.product_variants
                product_variant_ids.append(product_variant.id)

                if product_variant.promotion:
                    price = product_variant.promo_price
                elif product_variant.drop_shipping_price != 0:
                    price = product_variant.drop_shipping_price
                elif product_variant.wholesale_price != 0:
                    price = product_variant.wholesale_price
                else:
                    price = product_variant.default_price

                total_price += price * cart_item.quantity
                total_weight += product_variant.weight * cart_item.quantity

            except CartItem.DoesNotExist:
                continue
        print(total_weight)
        data['cost'] = total_price
        data['weight'] = total_weight
        data['tep_user'] = request.user.id
        data['product_variants'] = product_variant_ids

        service = get_delivery_service(service_type)
        response = service.create_parcel(data)
        return Response(response, status=status.HTTP_201_CREATED)


class GetWarehousesView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, service_type):
        service = get_delivery_service(service_type)
        response = service.get_warehouses(data=request.data)
        return Response(response, status=status.HTTP_200_OK)


class TrackParcelView(APIView):
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

