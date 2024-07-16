from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


class CartViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Cart instances.

    Attributes:
    - queryset: Queryset of all Cart instances.
    - permission_classes: List of permission classes that the view requires. Here, it ensures only authenticated users can access.
    - serializer_class: Serializer class used to serialize and deserialize Cart instances.
    - lookup_field: Field used for looking up individual cart instances, defaulting to 'id'.

    Actions:
    - Allows standard CRUD operations (create, retrieve, update, delete) on Cart instances.
    """

    queryset = Cart.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    lookup_field = 'id'


class CartItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing CartItem instances.

    Attributes:
    - queryset: Queryset of all CartItem instances.
    - permission_classes: List of permission classes that the view requires. Here, it ensures only authenticated users can access.
    - serializer_class: Serializer class used to serialize and deserialize CartItem instances.
    - lookup_field: Field used for looking up individual cart item instances, defaulting to 'id'.

    Actions:
    - Allows standard CRUD operations (create, retrieve, update, delete) on CartItem instances.

    """

    queryset = CartItem.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer
    lookup_field = 'id'
