"""Service to handle payments by LiqPay."""
from typing import Optional

from django.conf import settings
from liqpay import LiqPay


class LiqPayService:
    """Service to handle payments by LiqPay."""
    def __init__(self) -> None:
        self.liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
    
    def create_payment_template_data(self, amount: float, order_id: int, server_host: str, shipment_data: dict) -> str:
        """
        Create payment link.

        :param amount: amount to pay in UAH.
        :param order_id: id of order to pay.
        :param server_host: server host.
        :param shipment_data: information used to create parcel after confirm.

        :return: payment link.
        """
        server_url = f"{server_host}/api/post/payment/callback?order_id={order_id}&" \
             f"area_recipient={shipment_data.get('area_recipient', '')}&" \
             f"city_recipient={shipment_data.get('city_recipient', '')}&" \
             f"recipient_address={shipment_data.get('recipient_address', '')}&" \
             f"recipient_float={shipment_data.get('recipient_float', '')}&" \
             f"recipient_house={shipment_data.get('recipient_house', '')}&" \
             f"recipient_name={shipment_data.get('recipient_name', '')}&" \
             f"recipients_phone={shipment_data.get('recipients_phone', '')}&" \
             f"service_type={shipment_data.get('service_type', '')}&" \
             f"settlemen_type={shipment_data.get('settlemen_type', '')}"

        params = {
            'action': 'pay',
            'amount': f'{amount}',
            'currency': 'UAH',
            'description': f'Payment for order {order_id}',
            'order_id': order_id,
            'version': '3',
            'server_url': f'https://{server_url}',
            'result_url': f'https://{server_host}/purchase/confirmation', # success page
        }

        return  {
            'data': self.liqpay.cnb_data(params | shipment_data),
            'signature':  self.liqpay.cnb_signature(params | shipment_data),
        }

    def verify_payment(self, signature: str, liqpay_data: str) -> Optional[int]:
        """
        Verify if payment is valid.

        :param signature: liqpay signature.
        :param liqpay_data: decoded data send in request body by LiqPay.

        :return liqpay_decoded_data: decoded data of success response.
        """
        sign = self.liqpay.str_to_sign(settings.LIQPAY_PRIVATE_KEY + liqpay_data + settings.LIQPAY_PRIVATE_KEY)

        if sign == signature:
            liqpay_decoded_data = self.liqpay.decode_data_from_str(liqpay_data)

            return liqpay_decoded_data
