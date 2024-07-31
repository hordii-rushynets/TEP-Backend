from abc import ABC, abstractmethod


class AbstractDeliveryService(ABC):

    @abstractmethod
    def create_parcel(self, data):
        pass

    @abstractmethod
    def get_warehouses(self, city):
        pass

    @abstractmethod
    def track_parcel(self, tracking_number):
        pass

    @abstractmethod
    def calculate_delivery_cost(self, data):
        pass