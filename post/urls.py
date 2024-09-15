from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import (
    CalculateDeliveryCostView,
    CreateParcelView,
    GetWarehousesView,
    OrderViewSet,
    TrackParcelView,
    VerifyPaymentView
)


router = DefaultRouter()
router.register(r'orders', OrderViewSet)

urlpatterns = router.urls + [
    path('create-parcel/<str:service_type>/', CreateParcelView.as_view(), name='create_parcel'),
    path('get-warehouses/<str:service_type>/', GetWarehousesView.as_view(), name='get_warehouses'),
    path('track-parcel/<str:tracking_number>/', TrackParcelView.as_view(), name='track_parcel'),
    path('payment/callback', VerifyPaymentView.as_view(), name='validate_payment'),
    path('calculate-delivery-cost/<str:service_type>/', CalculateDeliveryCostView.as_view(),
         name='calculate_delivery_cost'),
]

