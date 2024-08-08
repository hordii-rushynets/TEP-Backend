import os
import requests
from .abstract_delivery_service import AbstractDeliveryService
from deep_translator import GoogleTranslator
from rest_framework.exceptions import ValidationError
from ..models import Order
from django.contrib.auth import get_user_model

User = get_user_model()


class UkrPoshtaDeliveryService(AbstractDeliveryService):
    def __init__(self):
        self.__base_get_warehouses_url = 'https://www.ukrposhta.ua/address-classifier-ws/'

    def track_parcel(self, tracking_number):
        url_uk = f'https://www.ukrposhta.ua/status-tracking/0.0.1/statuses?barcode={tracking_number}'
        url_en = url_uk + '&lang=en'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {os.getenv("UKR_POST_TRACK_PARCEL_API_KEY")}',
        }

        response_uk = requests.get(url_uk, headers=headers)
        response_en = requests.get(url_en, headers=headers)
        data = []
        print(response_uk.status_code)

        if response_uk.status_code == 200 and response_en.status_code == 200:
            uk_data = response_uk.json()
            en_data = response_en.json()
            for i, j in zip(uk_data, en_data):
                data.append({
                    'status_uk': i.get('eventName'),
                    'status_en': j.get('eventName'),
                    'status_ru': GoogleTranslator(source='uk', target='ru').translate(i.get('eventName')),
                    'update_date': i.get('date')
                })
            return data
        else:
            raise ValidationError('tracking number is invalid')

    def __get_region_id(self, region_name):
        headers = {
            'Accept': 'application/json',
        }

        url = f'{self.__base_get_warehouses_url}get_regions_by_region_ua?region_name={region_name}'
        request = requests.get(url, headers=headers)
        if request.status_code == 200:
            id = request.json().get('Entries').get('Entry')[0].get('REGION_ID')
            return id
        else:
            raise ValidationError('region_name is invalid')

    def __get_district_id(self, region_name, district_name):
        headers = {
            'Accept': 'application/json',
        }
        region_id = self.__get_region_id(region_name)
        url = f'{self.__base_get_warehouses_url}get_districts_by_region_id_and_district_ua?region_id={region_id}&district_ua={district_name}'
        request = requests.get(url, headers=headers)
        if request.status_code == 200:
            id = request.json().get('Entries').get('Entry')[0].get('DISTRICT_ID')
            return id
        else:
            raise ValidationError('district_name is invalid')

    def __get_city_id(self, region_name, district_name, city_name):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {os.getenv("UKR_POST_ECOM_API_KEY")}'
        }
        district_id = self.__get_district_id(region_name, district_name)
        url = f'{self.__base_get_warehouses_url}get_city_by_region_id_and_district_id_and_city_ua?district_id={district_id}&city_ua={city_name}'
        request = requests.get(url, headers=headers)
        if request.status_code == 200:
            id = request.json().get('Entries').get('Entry')[0].get('CITY_ID')
            return id
        else:
            raise ValidationError('city_name is invalid')

    def get_warehouses(self, data: dict):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {os.getenv("UKR_POST_ECOM_API_KEY")}'
        }
        city_id = self.__get_city_id(data.get("region_name"), data.get("district_name"), data.get("city_name"))
        url = f'{self.__base_get_warehouses_url}get_postoffices_by_postcode_cityid_cityvpzid?city_id={city_id}'
        request = requests.get(url, headers=headers)
        input_data = request.json().get('Entries').get('Entry')
        output_data = []
        if request.status_code == 200:
            for i in input_data:
                description = f'{i.get("POSTCODE")}: {i.get("CITY_UA_TYPE")} {i.get("CITY_UA")}, {i.get("STREET_UA_VPZ")}'
                output_data.append({
                    "description_uk": description,
                    "description_ru": GoogleTranslator(source='uk', target='ru').translate(description),
                    "description_en": GoogleTranslator(source='uk', target='en').translate(description),
                    "number": f'{i.get("POSTCODE")}'
                })
            return output_data
        else:
            raise ValidationError({request.json().get("message")})

    def __g_to_kg(self, number):
        if type(number) is str:
            try:
                return float(number) * 1000
            except ValueError:
                raise ValidationError(f'in the weight value, the fraction is denoted by "." instead of ",", or value '
                                      f'is not number')
        elif type(number) is int or type(number) is float:
            return number * 1000
        else:
            raise ValidationError(f"{number} is invalid")

    def calculate_delivery_cost(self, data):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {os.getenv("UKR_POST_ECOM_API_KEY")}',
            'Content-Type': 'application/json',
        }
        url = 'https://dev.ukrposhta.ua/ecom/0.0.1/domestic/delivery-price/'
        try:
            calculate_data = {
                "addressFrom": {"postcode": "58023"},
                "addressTo": {"postcode": data.get('city_recipient')},
                "type": "STANDARD",
                "validate": True,
                "deliveryType": "W2W",
                "weight": self.__g_to_kg(data.get('weight')),
                "length": data.get('length'),
                "declaredPrice": data.get('cost'),
            }

            request = requests.post(url=url, json=calculate_data, headers=headers)
            if request.status_code == 200:
                return {
                    "cost": request.json().get("deliveryPrice")
                }
            else:
                raise ValidationError({request.json().get("message")})
        except ValueError:
            raise ValidationError("")

    def __get_address_recipient_id(self, data):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {os.getenv("UKR_POST_ECOM_API_KEY")}',
            'Content-Type': 'application/json',
        }

        url = 'https://www.ukrposhta.ua/ecom/0.0.1/addresses/'
        request_data = {
            "postcode": data.get("city_recipient"),
            "country": "UA",
            "region": data.get("area_recipient"),
            "city": data.get("city_recipient"),
            "district": data.get("district"),
            "street": data.get("recipient_address"),
            "houseNumber": data.get("recipient_house"),
            "apartmentNumber": data.get("recipient_float")
        }

        data_from_ukr_post_api = requests.post(url=url, json=request_data, headers=headers)
        if data_from_ukr_post_api.status_code == 200:
            return data_from_ukr_post_api.json().get("id")
        else:
            raise ValidationError({data_from_ukr_post_api.json().get("message")})

    def __get_recipient_uuid(self, data):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {os.getenv("UKR_POST_ECOM_API_KEY")}',
            'Content-Type': 'application/json',
        }

        url = f'https://www.ukrposhta.ua/ecom/0.0.1/clients?token={os.getenv("UKR_POST_PROD_COUNTERPARTY_TOKEN")}'
        address_id = self.__get_address_recipient_id(data)
        recipient_name = data.get('recipient_name')
        recipient_full_name = []
        if recipient_name is not None:
            recipient_full_name = recipient_name.split(' ')
            if len(recipient_full_name) != 3:
                raise ValidationError('recipient_name is invalid')

        request_data = {
            "type": "INDIVIDUAL",
            "firstName": recipient_full_name[1],
            "lastName": recipient_full_name[0],
            "addressId": f"{address_id}",
            "phoneNumber": data.get('recipients_phone'),
            "email": data.get('recipients_email'),
        }

        data_from_ukr_post_api = requests.post(url=url, json=request_data, headers=headers)

        if data_from_ukr_post_api.status_code == 200:
            return data_from_ukr_post_api.json().get('uuid')
        else:
            raise ValidationError(data_from_ukr_post_api.json().get("message"))

    def create_parcel(self, data):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {os.getenv("UKR_POST_ECOM_API_KEY")}',
            'Content-Type': 'application/json',
        }

        url = f'https://www.ukrposhta.ua/ecom/0.0.1/shipments?token={os.getenv("UKR_POST_PROD_COUNTERPARTY_TOKEN")}'
        recipient_uuid = self.__get_recipient_uuid(data)

        request_data = {
            "sender": {"uuid": "a073fa4a-152f-45c5-9c4d-470b3aaa1f32"},
            "recipient": {"uuid": f"{recipient_uuid}"},
            "deliveryType": data.get("service_type"),
            "paidByRecipient": False,
            "type": "STANDARD",
            "declaredPrice": data.get("cost"),
            "parcels": [{
                "weight": self.__g_to_kg(data.get('weight')),
                "length": data.get("length"),
            }],
            "sms": True
        }

        data_from_ukr_post_api = requests.post(url=url, json=request_data, headers=headers)
        if data_from_ukr_post_api.status_code == 200:
            try:
                tep_user = User.objects.get(id=data['tep_user'])
            except User.DoesNotExist:
                raise ValidationError({"error": "TEPUser does not exist"})

            order = Order.objects.create(
                number=data_from_ukr_post_api.json().get("barcode"),
                tep_user=tep_user,
                post_type="UkrPost"
            )

            product_variants = data.get('product_variants', [])
            order.product_variant.add(*product_variants)

            return {"number": data_from_ukr_post_api.json().get("barcode"),
                    "price": data_from_ukr_post_api.json().get("rawDeliveryPrice")}
        else:
            raise ValidationError(data_from_ukr_post_api.json().get("message"))
