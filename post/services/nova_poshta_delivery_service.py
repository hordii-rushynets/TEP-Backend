import os
import requests

from deep_translator import GoogleTranslator
from django.conf import settings
from rest_framework.exceptions import ValidationError

from .constants import *
from .abstract_delivery_service import AbstractDeliveryService, create_order


class NovaPoshtaService(AbstractDeliveryService):
    api_url = "https://api.novaposhta.ua/v2.0/json/"
    api_key = os.getenv('NOVA_POST_API_KEY')

    def create_parcel(self, parcel_details: dict) -> dict:
        sender_contact = self.__get_contact_sender()

        payload = {
            "apiKey": self.api_key,
            "modelName": "InternetDocumentGeneral",
            "calledMethod": "save",
            "methodProperties": {
                "CitySender": os.getenv('REF_CITY_SENDER'),
                "SenderAddress": os.getenv('REF_ADDRESS_SENDER'),
                "Sender": os.getenv('REF_SENDER'),
                "ContactSender": sender_contact['ref'],
                "SendersPhone": sender_contact['phones'],

                "RecipientsPhone": parcel_details.get("recipients_phone", ""),
                "RecipientCityName": parcel_details.get('city_recipient', ""),
                "RecipientArea": parcel_details.get('area_recipient', ""),
                "RecipientAreaRegions": parcel_details.get('area_regions_recipient', ""),
                "RecipientAddressName": parcel_details.get('recipient_address', ""),
                "RecipientHouse": parcel_details.get('recipient_house', ""),
                "RecipientFlat": parcel_details.get('recipient_flat', ""),
                "RecipientName": parcel_details.get('recipient_name', ""),
                "RecipientType": "PrivatePerson",
                "SettlementType": parcel_details.get('settlemen_type', ""),
                "RecipientAddressNote": parcel_details.get("recipient_address_note", ""),

                "CargoType": "Parcel",
                "SeatsAmount": "1",
                "ServiceType": parcel_details.get("service_type", ""),

                "PayerType": "Recipient",
                "PaymentMethod": "Cash",
                "Description": parcel_details['description'],
                "Cost": parcel_details['cost'],
                "NewAddress": "1",
                "Weight": parcel_details.get('weight')
            }
        }

        response = requests.post(self.api_url, json=payload).json()
        if response.get('success'):
            parcel = response.get('data')[0]
            number = parcel.get('IntDocNumber')
            price = parcel.get('CostOnSite')

            create_order(parcel_details.get('tep_user'), number,
                         "NovaPost", parcel_details.get('product_variants', []))

            return {"number": number,
                    "price": price}
        else:
            errors_list = response.get('errors')
            errors_rename = []
            self.__error_rename(errors_list, errors_rename)
            raise ValidationError(errors_rename)

    def get_warehouses(self, search_data: dict) -> list[dict] | None:
        city_ref = self.__get_city_ref(search_data.get('city_name'))
        if not city_ref:
            return None

        payload = {
            "apiKey": self.api_key,
            "modelName": "AddressGeneral",
            "calledMethod": "getWarehouses",
            "methodProperties": {
                "CityRef": city_ref
            }
        }
        response = requests.post(self.api_url, json=payload, timeout=10).json()
        if response.get('success'):
            warehouses = []
            for warehouse in response.get('data'):
                if warehouse.get('CategoryOfWarehouse') == nova_post_branch:
                    warehouses.append({
                        "description_uk": warehouse.get('Description'),
                        "description_ru": warehouse.get('DescriptionRu'),
                        "description_en": GoogleTranslator(source='uk', target='en').translate(warehouse.get('Description')),
                        "number": warehouse.get('Number')
                    })
            return warehouses
        else:
            raise ValidationError(response.get('errors'))

    def track_parcel(self, tracking_number: str) -> list[dict]:
        payload = {
            "apiKey": self.api_key,
            "modelName": "TrackingDocument",
            "calledMethod": "getStatusDocuments",
            "methodProperties": {
                "Documents": [
                    {"DocumentNumber": tracking_number}
                ]
            }
        }
        response = requests.post(self.api_url, json=payload).json()

        if response.get('success'):
            parcel = response.get('data')[0]
            return [
                {
                    "status_uk": "Замовлення створено",
                    "status_en": "Order created",
                    "status_ru": "Заказ создан",
                    "update_date": parcel.get('DateCreated')
                },
                {
                    "status_uk": parcel.get('Status'),
                    "status_en": GoogleTranslator(source='uk', target='en').translate(parcel.get('Status')),
                    "status_ru": GoogleTranslator(source='uk', target='ru').translate(parcel.get('Status')),
                    "update_date": parcel.get('TrackingUpdateDate'),
                }
            ]
        else:
            raise ValidationError(tracking_number_error)

    def calculate_delivery_cost(self, data: dict) -> dict:
        city_recipient_ref = self.__get_city_ref(data.get('city_recipient'))
        if not city_recipient_ref:
            raise ValidationError({"error": "City recipient reference not found"})

        payload = {
            "apiKey": self.api_key,
            "modelName": "InternetDocument",
            "calledMethod": "getDocumentPrice",
            "methodProperties": {
                "CitySender": settings.REF_CITY_SENDER,
                "CityRecipient": city_recipient_ref,
                "Weight": data.get('weight'),
                "ServiceType": 'WarehouseWarehouse',
                "Cost": data.get('cost'),
                "CargoType": 'Parcel',
                "SeatsAmount": '1',
            }
        }
        response = requests.post(self.api_url, json=payload).json()

        if response.get('success'):
            delivery = response.get('data')[0]
            return {"cost": delivery.get("Cost")}
        else:
            raise ValidationError(response.get('errors'))

    def __get_city_ref(self, city: str) -> str | None:
        if not city:
            raise ValidationError(city_error)

        payload = {
            "apiKey": self.api_key,
            "modelName": "Address",
            "calledMethod": "getCities",
            "methodProperties": {
                "FindByString": city
            }
        }
        response = requests.post(self.api_url, json=payload, timeout=10).json()
        city_info = response.get('data')
        if response.get('success') and city_info:
            return city_info[0].get('Ref')
        elif len(city_info) == 0:
            raise ValidationError(city_error)

    def __error_rename(self, errors: list, data: list):
        for error in errors:
            error_name = error.split(' ')[0]
            rename_error = nova_post_error_rename.get(error_name, None)
            if rename_error is not None:
                data.append(rename_error)

    def __get_contact_sender(self) -> dict:
        payload = {
            "apiKey": self.api_key,
            "modelName": "CounterpartyGeneral",
            "calledMethod": "getCounterpartyContactPersons",
            "methodProperties": {
                "Ref": f"{os.getenv('REF_SENDER')}",
                "Page": "1"
            }
        }

        response = requests.post(self.api_url, json=payload).json()
        contact_sender = response.get('data')[2]
        return {
            "ref": contact_sender.get('Ref'),
            "phones": contact_sender.get('Phones')
        }
