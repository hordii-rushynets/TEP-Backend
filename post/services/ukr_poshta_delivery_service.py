import requests
from .abstract_delivery_service import AbstractDeliveryService
from django.conf import settings


class UkrPostDeliveryService(AbstractDeliveryService):
    BASE_URL = 'https://www.ukrposhta.ua/ecom/0.0.1'

    def __init__(self):
        self.api_key = settings.URK_POST_API_KEY
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def create_parcel(self, data):
        """
        Create a parcel in Ukr Post system.
        :return: JSON response from the API
        """
        response_data = {
            "sender": {
                "name": data['sender_name'],
                "phone": data['sender_phone'],
                "address": data['sender_address']
            },
            "recipient": {
                "name": data['recipient_name'],
                "phone": data['recipient_phone'],
                "address": data['recipient_address']
            },
            "weight": data['weight'],
            "dimensions": {
                "length": data['length'],
                "width": data['width'],
                "height": data['height']
            },
            "description": data['description']
        }

        url = f'{self.BASE_URL}/parcels'
        response = requests.post(url, headers=self.headers, json=response_data)
        if response.status_code == 201:
            return response.json()
        else:
            response.raise_for_status()

    def get_warehouses(self, city):
        url = f"{self.BASE_URL}offices?city={city}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def track_parcel(self, tracking_number):
        url = f'{self.BASE_URL}/track/{tracking_number}'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def calculate_delivery_cost(self, data):
        url = f"{self.BASE_URL}calculate"
        payload = {
            "senderCity": data['sender_city'],
            "recipientCity": data['recipient_city'],
            "weight": data['weight'],
            "length": data["length"],
            "width": data["width"],
            "height": data["height"]
        }
        response = requests.post(url, json=payload, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
