from abc import ABC

from django.contrib.auth import get_user_model

from ..models import Order, OrderItem

User = get_user_model()


def create_order(tep_user_id: int, number: str, post_type: str, order_item_data: list[dict]):
    tep_user = User.objects.get(id=tep_user_id)

    order = Order.objects.create(
        number=number,
        tep_user=tep_user,
        post_type=post_type
    )

    order_items = []
    for item_data in order_item_data:
        order_item = OrderItem(
            product_variant_id=item_data['product_variant_id'],
            color_id=item_data.get('color_id'),
            material_id=item_data.get('material_id'),
            size_id=item_data.get('size_id'),
            quantity=item_data['quantity']
        )
        order_item.save()
        order_items.append(order_item)

    order.order_item.set(order_items)


class AbstractDeliveryService(ABC):
    """Abstract factory for email services """
    def create_parcel(self, data: dict) -> dict:
        """Creating a parcel"""
        raise NotImplementedError

    def get_warehouses(self, data: dict) -> dict:
        """Receiving all post offices in the original city"""
        raise NotImplementedError

    def track_parcel(self, tracking_number: str) -> dict:
        """Tracking a parcel by its number"""
        raise NotImplementedError

    def calculate_delivery_cost(self, data: dict) -> dict:
        """Calculating the cost of delivery"""
        raise NotImplementedError
