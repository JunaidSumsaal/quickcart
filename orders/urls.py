from django.urls import path
from .views import cancel_order, order_details, place_order, order_list, order_detail, order_confirmation, track_order

urlpatterns = [
    path("place/", place_order, name="place-order"),
    path("", order_list, name="order-list"),
    path("<int:order_id>/", order_detail, name="order-detail"),
    path("confirmation/<int:order_id>/", order_confirmation, name="confirm-order"),
    path('track/<int:order_id>/', track_order, name='track-order'),
    path("cancel/<int:order_id>/", cancel_order, name="cancel-order"),
    path("details/<int:order_id>/", order_details, name="order-details"),
]
