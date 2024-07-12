from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Cart
from .serializers import CartSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    #permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    lookup_field = 'id'
