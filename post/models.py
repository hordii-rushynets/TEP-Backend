from django.db import models
from tep_user.models import TEPUser


class OrderNumber(models.Model):
    number = models.CharField(max_length=100)
    tep_user = models.ForeignKey(TEPUser, on_delete=models.CASCADE, related_name='order_number')
    post_type = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.post_type}: {self.number}"