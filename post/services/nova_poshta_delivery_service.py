import requests
from django.conf import settings
import os


class NovaPoshtaService:
    api_url = "https://api.novaposhta.ua/v2.0/json/"
    api_key = settings.NOVA_POST_API_KEY

    @staticmethod
    def get_city_ref(city_name: str) -> str | None:
        payload = {
            "apiKey": NovaPoshtaService.api_key,
            "modelName": "Address",
            "calledMethod": "getCities",
            "methodProperties": {
                "FindByString": city_name
            }
        }
        response = requests.post(NovaPoshtaService.api_url, json=payload, timeout=10)
        data = response.json()
        if data['success'] and data['data']:
            return data['data'][0]['Ref']
        return None

    @staticmethod
    def get_contact_sender(sender_ref: str) -> dict:
        payload = {
            "apiKey": "00e3c70569ef56571b32626d9a8d3a9f",
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

    @staticmethod
    def create_parcel(data: dict) -> dict:
        sender_contact = NovaPoshtaService.get_contact_sender("19b4de7e-c0d6-11e4-a77a-005056887b8d")

        print(data)

        payload = {
            "apiKey": NovaPoshtaService.api_key,
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
                "RecipientArea":  data.get('area_recipient', ""),
                "RecipientAreaRegions": data.get('area_regions_recipient', ""),
                "RecipientAddressName": data.get('recipient_address', ""),
                "RecipientHouse": data.get('recipient_house', ""),
                "RecipientFlat": data.get('recipient_float', ""),
                "RecipientName": data.get('recipient_name', ""),
                "RecipientType": "PrivatePerson",
                "SettlementType": data.get('settlemen_type', ""),
                "RecipientAddressNote": data.get("recipient_address_note", ""),

                "CargoType": "Parcel",
                "SeatsAmount": "1",
                "ServiceType":  data.get("service_type", ""),

                "PayerType": "Recipient",
                "PaymentMethod": "Cash",
                "Description": data['description'],
                "Cost": data['cost'],
                "NewAddress": "1",
                "Weight": data['weight']
            }
        }

        response = requests.post(NovaPoshtaService.api_url, json=payload)
        if response.json()['success']:
            data = {
                "status": response.json()['success'],
                "number": response.json()['data'][0]['IntDocNumber'],
                "priсe": response.json()['data'][0]['CostOnSite']
            }
        else:
            data = {
                "errors": response.json()['errors']
            }
        return data

    @staticmethod
    def get_warehouses(city_name: str) -> list[dict] | None:
        a = NovaPoshtaService()
        city_ref = a.get_city_ref(city_name)
        if not city_ref:
            return None

        payload = {
            "apiKey": NovaPoshtaService.api_key,
            "modelName": "AddressGeneral",
            "calledMethod": "getWarehouses",
            "methodProperties": {
                "CityRef": city_ref
            }
        }
        response = requests.post(NovaPoshtaService.api_url, json=payload, timeout=10)

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

    @staticmethod
    def track_parcel(tracking_number: str) -> list[dict]:
        payload = {
            "apiKey": NovaPoshtaService.api_key,
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

    @staticmethod
    def calculate_delivery_cost(data: dict) -> dict:
        a = NovaPoshtaService()
        city_recipient_ref = a.get_city_ref(data['city_recipient'])
        if not city_recipient_ref:
            return {"error": "City recipient reference not found"}

        payload = {
            "apiKey": NovaPoshtaService.api_key,
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
        response = requests.post(NovaPoshtaService.api_url, json=payload)
        response_data = response.json()

        data = {
            "cost": response_data["data"][0]["Cost"]
        }
        return data
