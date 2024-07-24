from rest_framework import serializers


class CreateParcelSerializer(serializers.Serializer):
    payer_type = serializers.CharField(max_length=50)
    payment_method = serializers.CharField(max_length=50)
    date_time = serializers.DateTimeField()
    cargo_type = serializers.CharField(max_length=50)
    volume_general = serializers.FloatField()
    weight = serializers.FloatField()
    service_type = serializers.CharField(max_length=50)
    seats_amount = serializers.IntegerField()
    description = serializers.CharField(max_length=255)
    cost = serializers.FloatField()
    city_sender = serializers.CharField(max_length=255)
    sender = serializers.CharField(max_length=255)
    sender_address = serializers.CharField(max_length=255)
    contact_sender = serializers.CharField(max_length=255)
    senders_phone = serializers.CharField(max_length=50)
    city_recipient = serializers.CharField(max_length=255)
    recipient = serializers.CharField(max_length=255)
    recipient_address = serializers.CharField(max_length=255)
    contact_recipient = serializers.CharField(max_length=255)
    recipients_phone = serializers.CharField(max_length=50)


class CitySerializer(serializers.Serializer):
    city_name = serializers.CharField(max_length=255)

