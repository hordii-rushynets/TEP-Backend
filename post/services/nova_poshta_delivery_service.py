import requests
from django.conf import settings
import os
from .Post_Error import nova_post_error_rename
from django.contrib.auth import get_user_model
from ..models import OrderNumber
from rest_framework.exceptions import ValidationError

User = get_user_model()


class NovaPoshtaService:
    api_url = "https://api.novaposhta.ua/v2.0/json/"
    api_key = settings.NOVA_POST_API_KEY

    def get_city_ref(self, city_name: str) -> str | None:
        payload = {
            "apiKey": self.api_key,
            "modelName": "Address",
            "calledMethod": "getCities",
            "methodProperties": {
                "FindByString": city_name
            }
        }
        response = requests.post(self.api_url, json=payload, timeout=10)
        data = response.json()
        if data['success'] and data['data']:
            return data['data'][0]['Ref']
        return None

    def error_rename(self, errors: list, data: list) -> list:
        for i in errors:
            error_name = i.split(' ')[0]
            rename_error = nova_post_error_rename.get(error_name, None)
            if rename_error is not None:
                data.append(rename_error)
        return data

    def get_contact_sender(self, sender_ref: str) -> dict:
        payload = {
            "apiKey": self.api_key,
            "modelName": "CounterpartyGeneral",
            "calledMethod": "getCounterpartyContactPersons",
            "methodProperties": {
                "Ref": f"{sender_ref}",
                "Page": "1"
            }
        }

        response = requests.post(NovaPoshtaService.api_url, json=payload)

        data = {
            "ref": response.json()['data'][2]['Ref'],
            "phones": response.json()['data'][2]['Phones']
        }
        return data

    def create_parcel(self, data: dict) -> dict:
        sender_contact = self.get_contact_sender(os.getenv('REF_SENDER'))

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

                "RecipientsPhone": data.get("recipients_phone", ""),
                "RecipientCityName": data.get('city_recipient', ""),
                "RecipientArea": data.get('area_recipient', ""),
                "RecipientAreaRegions": data.get('area_regions_recipient', ""),
                "RecipientAddressName": data.get('recipient_address', ""),
                "RecipientHouse": data.get('recipient_house', ""),
                "RecipientFlat": data.get('recipient_flat', ""),
                "RecipientName": data.get('recipient_name', ""),
                "RecipientType": "PrivatePerson",
                "SettlementType": data.get('settlemen_type', ""),
                "RecipientAddressNote": data.get("recipient_address_note", ""),

                "CargoType": "Parcel",
                "SeatsAmount": "1",
                "ServiceType": data.get("service_type", ""),

                "PayerType": "Recipient",
                "PaymentMethod": "Cash",
                "Description": data['description'],
                "Cost": data['cost'],
                "NewAddress": "1",
                "Weight": data['weight']
            }
        }

        response = requests.post(self.api_url, json=payload)
        if response.json()['success']:
            try:
                tep_user = User.objects.get(id=data['tep_user'])
            except User.DoesNotExist:
                raise ValidationError({"error": "TEPUser does not exist"})

            order_number = OrderNumber.objects.create(
                number=response.json()['data'][0]['IntDocNumber'],
                tep_user=tep_user,
                post_type="NovaPost"
            )

            data = {
                "status": response.json()['success'],
                "number": order_number.number,
                "price": response.json()['data'][0]['CostOnSite'],
            }
        else:
            data = []
            data.append({'status': response.json()['success']})
            errors_list = response.json()['errors']
            self.error_rename(errors_list, data)

        return data

    def get_warehouses(self, city_name: str) -> list[dict] | None:
        a = NovaPoshtaService()
        city_ref = a.get_city_ref(city_name)
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
        response = requests.post(self.api_url, json=payload, timeout=10)

        data = []

        for i in response.json()['data']:
            if i['CategoryOfWarehouse'] == "Branch":
                data.append({
                    "description_uk": i['Description'],
                    "description_ru": i['DescriptionRu'],
                    "description_en": i['Description'],
                    "number": i['Number']
                })

        return data

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
        response = requests.post(NovaPoshtaService.api_url, json=payload)
        data = [
            {
                "status_uk": "Замовлення створено",
                "status_en": "Order created",
                "status_ru": "Заказ создан",
                "update_date": response.json()['data'][0]['DateCreated']
            },
            {
                "status_uk": response.json()['data'][0]['Status'],
                "status_en": response.json()['data'][0]['Status'],
                "status_ru": response.json()['data'][0]['Status'],
                "update_date": response.json()['data'][0]['TrackingUpdateDate'],
            }
        ]
        return data

    def calculate_delivery_cost(self, data: dict) -> dict:
        city_recipient_ref = self.get_city_ref(data['city_recipient'])
        if not city_recipient_ref:
            return {"error": "City recipient reference not found"}

        payload = {
            "apiKey": self.api_key,
            "modelName": "InternetDocument",
            "calledMethod": "getDocumentPrice",
            "methodProperties": {
                "CitySender": settings.REF_CITY_SENDER,
                "CityRecipient": city_recipient_ref,
                "Weight": data['weight'],
                "ServiceType": 'WarehouseWarehouse',
                "Cost": data['cost'],
                "CargoType": 'Parcel',
                "SeatsAmount": '1',
            }
        }
        response = requests.post(self.api_url, json=payload)
        response_data = response.json()

        if response.json()['success']:
            data = {
                "cost": response_data["data"][0]["Cost"]
            }
        else:
            data = []
            errors_list = response.json()['errors']
            self.error_rename(errors_list, data)
        return data
