import os
import requests

from deep_translator import GoogleTranslator
from rest_framework.exceptions import ValidationError

from .abstract_delivery_service import AbstractDeliveryService, create_order
from .constants import *


class UkrPoshtaDeliveryService(AbstractDeliveryService):
    def __init__(self):
        self.url = 'https://www.ukrposhta.ua/'
        self.headers = {
            'Accept': 'application/json',
        }

    def track_parcel(self, tracking_number):
        url_uk = f'{self.url}status-tracking/0.0.1/statuses?barcode={tracking_number}'
        url_en = url_uk + '&lang=en'

        headers = self.headers.copy()
        headers['Authorization'] = f'Bearer {os.getenv("UKR_POST_TRACK_PARCEL_API_KEY")}'

        response_uk = requests.get(url_uk, headers=headers)
        response_en = requests.get(url_en, headers=headers)

        if response_uk.status_code == 200 and response_en.status_code == 200:
            parcels = []
            parcel_uk = response_uk.json()
            parcel_en = response_en.json()
            for i, j in zip(parcel_uk, parcel_en):
                parcels.append({
                    'status_uk': i.get('eventName'),
                    'status_en': j.get('eventName'),
                    'status_ru': GoogleTranslator(source='uk', target='ru').translate(i.get('eventName')),
                    'update_date': i.get('date')
                })
            return parcels
        else:
            raise ValidationError('tracking number is invalid')

    def get_warehouses(self, search_data: dict):
        headers = self.headers.copy()
        headers['Authorization'] = f'Bearer {os.getenv("UKR_POST_ECOM_API_KEY")}'

        city_id = self.__get_city_id(search_data.get("region_name"), search_data.get("district_name"), search_data.get("city_name"))
        url = f'{self.url}/address-classifier-ws/get_postoffices_by_postcode_cityid_cityvpzid?city_id={city_id}'

        request = requests.get(url, headers=headers)
        warehouses = request.json().get('Entries').get('Entry')

        if request.status_code == 200:
            warehouses_info = []
            for warehouse in warehouses:
                description = (f'{warehouse.get("POSTCODE")}: {warehouse.get("CITY_UA_TYPE")} '
                               f'{warehouse.get("CITY_UA")}, {warehouse.get("STREET_UA_VPZ")}')
                warehouses_info.append({
                    "description_uk": description,
                    "description_ru": GoogleTranslator(source='uk', target='ru').translate(description),
                    "description_en": GoogleTranslator(source='uk', target='en').translate(description),
                    "number": f'{warehouse.get("POSTCODE")}'
                })
            return warehouses_info
        else:
            raise ValidationError({request.json().get("message")})

    def calculate_delivery_cost(self, data):
        headers = self.headers.copy()
        headers['Authorization'] = f'Bearer {os.getenv("UKR_POST_ECOM_API_KEY")}'

        url = f'{self.url}ecom/0.0.1/domestic/delivery-price/'

        calculate_data = {
            "addressFrom": {"postcode": os.getenv('UKR_POST_ADDRESS_FROM')},
            "addressTo": {"postcode": data.get('city_recipient')},
            "type": "STANDARD",
            "validate": True,
            "deliveryType": "W2W",
            "weight": self.__kg_to_g(data.get('weight')),
            "length": '20',
            "declaredPrice": data.get('cost'),
        }

        response = requests.post(url=url, json=calculate_data, headers=headers)
        delivery = response.json()
        if response.status_code == 200:
            return {"cost": delivery.get("deliveryPrice")}
        else:
            raise ValidationError(delivery.get("message"))

    def create_parcel(self, parcel_details):
        headers = self.headers.copy()
        headers['Authorization'] = f'Bearer {os.getenv("UKR_POST_ECOM_API_KEY")}'

        url = f'{self.url}ecom/0.0.1/shipments?token={os.getenv("UKR_POST_PROD_COUNTERPARTY_TOKEN")}'
        recipient_uuid = self.__get_recipient_uuid(parcel_details)

        request_data = {
            "sender": {"uuid": "a073fa4a-152f-45c5-9c4d-470b3aaa1f32"},
            "recipient": {"uuid": f"{recipient_uuid}"},
            "deliveryType": parcel_details.get("service_type"),
            "paidByRecipient": False,
            "type": "STANDARD",
            "declaredPrice": parcel_details.get("cost"),
            "parcels": [{
                "weight": self.__kg_to_g(parcel_details.get('weight')),
                "length": "50",
            }],
            "sms": True
        }

        response = requests.post(url=url, json=request_data, headers=headers)
        parcel = response.json()
        if response.status_code == 200:
            number = parcel.get("barcode")

            create_order(
                tep_user_id=parcel_details.get('tep_user'),
                number=number,
                post_type="NovaPost",
                order_item_data=parcel_details.get('order_item_data', [])
            )

            return {"number": number,
                    "price": parcel.get("rawDeliveryPrice")}
        else:
            raise ValidationError(parcel.get("message"))

    def __id_or_error(self, response, name: str, error_name: str):
        if response.status_code == 200:
            return response.json().get('Entries').get('Entry')[0].get(name)
        else:
            raise ValidationError(response.text)

    def __get_region_id(self, region_name):
        url = f'{self.url}address-classifier-ws/get_regions_by_region_ua?region_name={region_name}'
        response = requests.get(url, headers=self.headers)

        return self.__id_or_error(response, 'REGION_ID', region_error)

    def __get_district_id(self, region_name, district_name):
        region_id = self.__get_region_id(region_name)
        url = f'{self.url}address-classifier-ws/get_districts_by_region_id_and_district_ua?region_id={region_id}&district_ua={district_name}'
        response = requests.get(url, headers=self.headers)

        return self.__id_or_error(response, 'DISTRICT_ID', district_error)

    def __get_city_id(self, region_name, district_name, city_name):
        headers = self.headers.copy()
        headers['Authorization'] = f'Bearer {os.getenv("UKR_POST_ECOM_API_KEY")}'

        district_id = self.__get_district_id(region_name, district_name)
        url = f'{self.url}address-classifier-ws/get_city_by_region_id_and_district_id_and_city_ua?district_id={district_id}&city_ua={city_name}'
        response = requests.get(url, headers=headers)

        return self.__id_or_error(response, 'CITY_ID', city_error)

    def __kg_to_g(self, number: str | int | float):
        """Сonverts kilograms into grams"""
        if type(number) is str:
            try:
                return float(number) * 1000
            except ValueError:
                raise ValidationError(f'in the weight value, the fraction is denoted by "." instead of ","')
        elif type(number) is int or type(number) is float:
            return number * 1000
        else:
            raise ValidationError(f"{number} is invalid")

    def __get_address_id(self, address_info):
        headers = self.headers.copy()
        headers['Authorization'] = f'Bearer {os.getenv("UKR_POST_ECOM_API_KEY")}'

        url = f'{self.url}ecom/0.0.1/addresses/'
        request_data = {
            "postcode": address_info.get("city_recipient"),
            "country": "UA",
            "region": address_info.get("area_recipient"),
            "city": address_info.get("city_recipient"),
            "district": address_info.get("district"),
            "street": address_info.get("recipient_address"),
            "houseNumber": address_info.get("recipient_house"),
            "apartmentNumber": address_info.get("recipient_float")
        }

        response = requests.post(url=url, json=request_data, headers=headers)
        address = response.json()
        if response.status_code == 200:
            return address.get("id")
        else:
            raise ValidationError(address.get("message"))

    def __get_recipient_uuid(self, data):
        headers = self.headers.copy()
        headers['Authorization'] = f'Bearer {os.getenv("UKR_POST_ECOM_API_KEY")}'

        url = f'{self.url}ecom/0.0.1/clients?token={os.getenv("UKR_POST_PROD_COUNTERPARTY_TOKEN")}'
        address_id = self.__get_address_id(data)
        recipient_name = data.get('recipient_name')
        recipient_full_name = []
        if recipient_name is not None:
            recipient_full_name = recipient_name.split(' ')
            if len(recipient_full_name) != 2:
                raise ValidationError(recipient_error)

        request_data = {
            "type": "INDIVIDUAL",
            "firstName": recipient_full_name[1],
            "lastName": recipient_full_name[0],
            "addressId": f"{address_id}",
            "phoneNumber": data.get('recipients_phone'),
            "email": data.get('recipients_email'),
        }

        response = requests.post(url=url, json=request_data, headers=headers)
        recipient = response.json()

        if response.status_code == 200:
            return recipient.get('uuid')
        else:
            raise ValidationError(recipient_error)
