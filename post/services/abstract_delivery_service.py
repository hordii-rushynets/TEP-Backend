from abc import ABC

from django.contrib.auth import get_user_model

from ..models import Order, OrderItem

User = get_user_model()


def create_order(tep_user: None, ip_address: str, post_type: str, order_item_data: list[dict], **kwargs):
    order = Order.objects.create(
        tep_user=tep_user,
        ip_address=ip_address,
        post_type=post_type,
        **kwargs
    )

    order_items = []
    for item_data in order_item_data:
        order_item = OrderItem(
            product_variant_id=item_data.get('product_variant_id'),
            color_id=item_data.get('color_id'),
            material_id=item_data.get('material_id'),
            size_id=item_data.get('size_id'),
            quantity=item_data.get('quantity')
        )

        order_item.save() # save to make many-to-many relationship

        filter_fields = item_data.get('filter_field_ids', [])
        if filter_fields:
            order_item.filter_fields.set(filter_fields)
            order_item.save()

        order_items.append(order_item)

    order.order_item.set(order_items)
    return order


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

    def delete_parcel(self, code: str) -> bool:
        """Removing a parcel from your personal post office account"""
        raise NotImplementedError
