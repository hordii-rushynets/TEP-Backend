# services/factory.py
from .nova_poshta_delivery_service import NovaPoshtaService
from .ukr_poshta_delivery_service import UkrPostDeliveryService


def get_delivery_service(service_type):
    if service_type == 'NovaPost':
        return NovaPoshtaService()
    elif service_type == 'UkrPost':
        return UkrPostDeliveryService()
    else:
        raise ValueError("Invalid service type")
