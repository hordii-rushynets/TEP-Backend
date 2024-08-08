from abc import ABC


class AbstractDeliveryService(ABC):

    def create_parcel(self, data: dict):
        pass

    def get_warehouses(self, data: dict):
        pass

    def track_parcel(self, tracking_number):
        pass

    def calculate_delivery_cost(self, data: dict):
        pass
