import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Payment
from orders.models import Order

# Checkout Page
@login_required
def checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    payment, created = Payment.objects.get_or_create(order=order, defaults={"amount": order.total_price, "payment_status": "pending"})
    
    if request.method == "POST":
        return redirect("process-payment", order_id=order.id)

    return render(request, "payments/checkout.html", {"order": order})

# Mock Payment Processing
@login_required
def process_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    payment, created = Payment.objects.get_or_create(order=order, amount=order.total_price)

    # Simulate a random payment status
    payment_status = random.choice(["paid", "failed"])
    payment.payment_status = payment_status
    payment.save()

    if payment_status != "paid":
        return redirect("payment-failed", order_id=order.id)
    order.status = "processing"
    order.save()
    return redirect("payment-success", order_id=order.id)

# Payment Success Page
@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "payments/payment_success.html", {"order": order})

# Payment Failed Page
@login_required
def payment_failed(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "payments/payment_failed.html", {"order": order})
