from django.urls import path
from .views import CreateParcelView, WarehousesView

urlpatterns = [
    path('create-parcel/', CreateParcelView.as_view(), name='create-parcel'),
    path('warehouses/', WarehousesView.as_view(), name='warehouses'),

]
