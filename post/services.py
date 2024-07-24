import requests
from django.conf import settings


class NovaPoshtaService:
    api_url = "https://api.novaposhta.ua/v2.0/json/"
    api_key = settings.NOVA_POST_API_KEY

    @staticmethod
    def get_city_ref(city_name):
        payload = {
            "apiKey": NovaPoshtaService.api_key,
            "modelName": "Address",
            "calledMethod": "getCities",
            "methodProperties": {
                "FindByString": city_name
            }
        }
        response = requests.post(NovaPoshtaService.api_url, json=payload)
        data = response.json()
        if data['success'] and data['data']:
            return data['data'][0]['Ref']
        return None

    @staticmethod
    def get_counterparty_ref(name):
        payload = {
            "apiKey": NovaPoshtaService.api_key,
            "modelName": "Counterparty",
            "calledMethod": "getCounterparties",
            "methodProperties": {
                "CounterpartyProperty": "Sender",
                "FindByString": name
            }
        }
        response = requests.post(NovaPoshtaService.api_url, json=payload)
        data = response.json()
        if data['success'] and data['data']:
            return data['data'][0]['Ref']
        return None

    @staticmethod
    def get_address_ref(address, city_ref):
        payload = {
            "apiKey": NovaPoshtaService.api_key,
            "modelName": "Address",
            "calledMethod": "getStreet",
            "methodProperties": {
                "CityRef": city_ref,
                "FindByString": address
            }
        }
        response = requests.post(NovaPoshtaService.api_url, json=payload)
        data = response.json()
        if data['success'] and data['data']:
            return data['data'][0]['Ref']
        return None

    @staticmethod
    def create_parcel(data):
        payload = {
            "apiKey": NovaPoshtaService.api_key,
            "modelName": "InternetDocument",
            "calledMethod": "save",
            "methodProperties": {
                "PayerType": data['payer_type'],
                "PaymentMethod": data['payment_method'],
                "DateTime": data['date_time'],
                "CargoType": data['cargo_type'],
                "VolumeGeneral": data['volume_general'],
                "Weight": data['weight'],
                "ServiceType": data['service_type'],
                "SeatsAmount": data['seats_amount'],
                "Description": data['description'],
                "Cost": data['cost'],
                "CitySender": data['city_sender_ref'],
                "Sender": data['sender_ref'],
                "SenderAddress": data['sender_address_ref'],
                "ContactSender": data['contact_sender_ref'],
                "SendersPhone": data['senders_phone'],
                "CityRecipient": data['city_recipient_ref'],
                "Recipient": data['recipient_ref'],
                "RecipientAddress": data['recipient_address_ref'],
                "ContactRecipient": data['contact_recipient_ref'],
                "RecipientsPhone": data['recipients_phone']
            }
        }
        response = requests.post(NovaPoshtaService.api_url, json=payload)
        return response.json()

    @staticmethod
    def get_warehouses(city_ref):
        payload = {
            "apiKey": NovaPoshtaService.api_key,
            "modelName": "AddressGeneral",
            "calledMethod": "getWarehouses",
            "methodProperties": {
                "CityRef": city_ref
            }
        }
        response = requests.post(NovaPoshtaService.api_url, json=payload)
        return response.json()
