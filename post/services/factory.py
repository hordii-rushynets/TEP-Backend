# services/factory.py
from .nova_poshta_delivery_service import NovaPoshtaService
from .ukr_poshta_delivery_service import UkrPoshtaDeliveryService
from rest_framework.exceptions import ValidationError


def get_delivery_service(service_type):
    if service_type == 'NovaPost':
        return NovaPoshtaService()
    elif service_type == 'UkrPost':
        return UkrPoshtaDeliveryService()
    else:
        raise ValidationError("Invalid service type")
