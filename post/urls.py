from django.urls import path
from .views import CreateParcelView, GetWarehousesView, TrackParcelView, CalculateDeliveryCostView

urlpatterns = [
    path('create-parcel/<str:service_type>/', CreateParcelView.as_view(), name='create_parcel'),
    path('get-warehouses/<str:service_type>/<str:city>/', GetWarehousesView.as_view(), name='get_warehouses'),
    path('track-parcel/<str:service_type>/', TrackParcelView.as_view(), name='track_parcel'),
    path('calculate-delivery-cost/<str:service_type>/', CalculateDeliveryCostView.as_view(),
         name='calculate_delivery_cost'),
]

