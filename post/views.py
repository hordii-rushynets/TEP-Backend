from .services.factory import get_delivery_service
from rest_framework import status, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response


class CreateParcelView(APIView):
    def post(self, request, service_type):
        data = request.POST
        service = get_delivery_service(service_type)
        response = service.create_parcel(data)
        return Response(response)


class GetWarehousesView(APIView):
    def get(self, request, service_type, city):
        service = get_delivery_service(service_type)
        try:
            response = service.get_warehouses(city)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TrackParcelView(APIView):
    def get(self, request, service_type):
        tracking_number = request.GET.get('tracking_number')
        service = get_delivery_service(service_type)
        response = service.track_parcel(tracking_number)
        return Response(response)


class CalculateDeliveryCostView(APIView):
    def post(self, request, service_type):
        data = request.POST
        service = get_delivery_service(service_type)
        response = service.calculate_delivery_cost(data)
        return Response(response)
