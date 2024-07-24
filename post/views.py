from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CreateParcelSerializer, CitySerializer
from .services import NovaPoshtaService


class CreateParcelView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = CreateParcelSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            nova_poshta_service = NovaPoshtaService()

            city_sender_ref = nova_poshta_service.get_city_ref(data['city_sender'])
            sender_ref = nova_poshta_service.get_counterparty_ref(data['sender'])
            sender_address_ref = nova_poshta_service.get_address_ref(data['sender_address'], city_sender_ref)
            contact_sender_ref = sender_ref
            city_recipient_ref = nova_poshta_service.get_city_ref(data['city_recipient'])
            recipient_ref = nova_poshta_service.get_counterparty_ref(data['recipient'])
            recipient_address_ref = nova_poshta_service.get_address_ref(data['recipient_address'], city_recipient_ref)
            contact_recipient_ref = recipient_ref

            parcel_data = {
                **data,
                'city_sender_ref': city_sender_ref,
                'sender_ref': sender_ref,
                'sender_address_ref': sender_address_ref,
                'contact_sender_ref': contact_sender_ref,
                'city_recipient_ref': city_recipient_ref,
                'recipient_ref': recipient_ref,
                'recipient_address_ref': recipient_address_ref,
                'contact_recipient_ref': contact_recipient_ref
            }

            response = nova_poshta_service.create_parcel(parcel_data)

            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WarehousesView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            city_name = serializer.validated_data['city_name']
            nova_poshta_service = NovaPoshtaService()

            city_ref = nova_poshta_service.get_city_ref(city_name)
            if not city_ref:
                return Response({"error": "City not found"}, status=status.HTTP_404_NOT_FOUND)

            response = nova_poshta_service.get_warehouses(city_ref)

            if response.get('success'):
                return Response(response['data'], status=status.HTTP_200_OK)
            else:
                return Response({"error": response.get('errors', "Unable to fetch warehouses")},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
