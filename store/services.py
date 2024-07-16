from datetime import date
from rest_framework.exceptions import ValidationError
from .models import ProductView


class PControlService:
    @staticmethod
    def check_ip_address(product, ip_address):
        if ProductView.objects.filter(product=product, ip_address=ip_address, view_date=date.today()).exists():
            raise ValidationError('You have already viewed this product today.')
