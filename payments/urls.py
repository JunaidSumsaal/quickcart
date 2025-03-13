from django.urls import path
from .views import checkout, process_payment, payment_success, payment_failed

urlpatterns = [
    path("checkout/<int:order_id>/", checkout, name="checkout"),
    path("process/<int:order_id>/", process_payment, name="process-payment"),
    path("success/<int:order_id>/", payment_success, name="payment-success"),
    path("failed/<int:order_id>/", payment_failed, name="payment-failed"),
    

]
