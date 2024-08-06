from .services.factory import get_delivery_service
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import OrderNumber
from rest_framework.permissions import IsAuthenticated, AllowAny


class CreateParcelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, service_type):
        try:
            data = request.data.copy()
            data['tep_user'] = request.user.id
            service = get_delivery_service(service_type)
            response = service.create_parcel(data)
            check = response[0].get('status', None)
            if check is False:
                response.pop(0)
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            elif check:
                return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetWarehousesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, service_type, city):
        try:
            service = get_delivery_service(service_type)
            response = service.get_warehouses(city)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TrackParcelView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, service_type, tracking_number):
        if not OrderNumber.objects.filter(number=tracking_number).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            service = get_delivery_service(service_type)
            response = service.track_parcel(tracking_number)
            return Response(response)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CalculateDeliveryCostView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, service_type):
        try:
            service = get_delivery_service(service_type)
            data = request.data
            response = service.calculate_delivery_cost(data)
            return Response(response)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
