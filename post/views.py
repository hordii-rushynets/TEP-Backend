from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .services.factory import get_delivery_service


class CreateParcelView(View):
    def post(self, request, service_type):
        data = request.POST
        service = get_delivery_service(service_type)
        response = service.create_parcel(data)
        return JsonResponse(response)


class GetWarehousesView(View):
    def get(self, request, service_type):
        city = request.GET.get('city')
        service = get_delivery_service(service_type)
        response = service.get_warehouses(city)
        return JsonResponse(response, safe=False)


class TrackParcelView(View):
    def get(self, request, service_type):
        tracking_number = request.GET.get('tracking_number')
        service = get_delivery_service(service_type)
        response = service.track_parcel(tracking_number)
        return JsonResponse(response)


class CalculateDeliveryCostView(View):
    def post(self, request, service_type):
        data = request.POST
        service = get_delivery_service(service_type)
        response = service.calculate_delivery_cost(data)
        return JsonResponse(response)
