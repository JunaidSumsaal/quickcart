from django.urls import path
from .views import place_order, order_list, order_detail, order_confirmation

urlpatterns = [
    path("place/", place_order, name="place-order"),
    path("confirmation/<int:order_id>/", order_confirmation, name="order-confirmation"),
    path("", order_list, name="order-list"),
    path("<int:order_id>/", order_detail, name="order-detail"),
]
