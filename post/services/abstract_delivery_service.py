from abc import ABC

from django.contrib.auth import get_user_model

from ..models import Order

User = get_user_model()


def create_order(tep_user_id: int, number: int, post_type: str, product_variants_ids: list[int]):
    tep_user = User.objects.get(id=tep_user_id)

    order = Order.objects.create(
        number=number,
        tep_user=tep_user,
        post_type=post_type
    )
    order.product_variant.add(*product_variants_ids)


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
