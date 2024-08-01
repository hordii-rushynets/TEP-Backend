import requests
from django.conf import settings
from requests.exceptions import SSLError


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
        response = requests.post(NovaPoshtaService.api_url, json=payload, timeout=10)
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
    def get_counterparty_addresses(counterparty_ref):
        payload = {
            "apiKey": NovaPoshtaService.api_key,
            "modelName": "CounterpartyGeneral",
            "calledMethod": "getCounterpartyAddresses",
            "methodProperties": {
                "Ref": counterparty_ref,
                "CounterpartyProperty": "Sender"
            }
        }
        response = requests.post(NovaPoshtaService.api_url, json=payload)
        data = response.json()
        if data['success'] and data['data']:
            return data['data']
        return None

    @staticmethod
    def get_warehouse_ref(city_name, warehouse_number):
        city_ref = NovaPoshtaService.get_city_ref(city_name)
        if not city_ref:
            return None

        warehouses = NovaPoshtaService.get_warehouses(city_name)
        if warehouses['success']:
            for warehouse in warehouses['data']:
                if warehouse['Number'] == warehouse_number:
                    return warehouse['Ref']
        return None

    @staticmethod
    def create_parcel(data):
        city_sender_ref = NovaPoshtaService.get_city_ref(data['city_sender'])
        city_recipient_ref = NovaPoshtaService.get_city_ref(data['city_recipient'])
        sender_ref = NovaPoshtaService.get_counterparty_ref(data['sender_name'])
        recipient_warehouse_ref = NovaPoshtaService.get_warehouse_ref(data['city_recipient'],
                                                                      data['recipient_warehouse_number'])
        sender_address_ref = NovaPoshtaService.get_address_ref(data['sender_address'], data['city_sender'])

        payload = {
            "apiKey": NovaPoshtaService.api_key,
            "modelName": "InternetDocument",
            "calledMethod": "save",
            "methodProperties": {
                "PayerType": data['payer_type'],
                "PaymentMethod": data['payment_method'],
                "CargoType": data['cargo_type'],
                "Weight": data['weight'],
                "ServiceType": data['service_type'],
                "SeatsAmount": data['seats_amount'],
                "Description": data['description'],
                "CitySender": city_sender_ref,
                "Sender": sender_ref,
                "SenderAddress": sender_address_ref,
                "ContactSender": data['contact_sender'],
                "SendersPhone": data['senders_phone'],
                "CityRecipient": city_recipient_ref,
                "RecipientWarehouse": recipient_warehouse_ref,
                "RecipientsPhone": data['recipient_phone']
            }
        }
        response = requests.post(NovaPoshtaService.api_url, json=payload)
        return response.json()

    @staticmethod
    def get_warehouses(city_name):
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
        return response.json()

    @staticmethod
    def track_parcel(tracking_number):
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
        return response.json()

    @staticmethod
    def get_address_ref(address, city_name):
        city_ref = NovaPoshtaService.get_city_ref(city_name)
        if not city_ref:
            return None

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
    def calculate_delivery_cost(data):
        try:
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

        except SSLError as e:
            return {"error": f"SSL error occurred: {str(e)}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Request exception occurred: {str(e)}"}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}
