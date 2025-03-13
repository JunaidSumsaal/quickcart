from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem, OrderTracking
from cart.models import Cart

@login_required
def place_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        return redirect("view-cart")

    order = Order.objects.create(user=request.user, status="pending")

    for item in cart.items.all():
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)

    order.update_total_price()
    cart.items.all().delete()

    return redirect("checkout", order_id=order.id)

@login_required
def track_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    tracking_updates = OrderTracking.objects.filter(order=order).order_by("-timestamp")

    return render(
        request,
        "orders/track_order.html",
        {
            "order": order,
            "order_items": order_items,
            "tracking_updates": tracking_updates,
        },
    )


# Order Confirmation Page
@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/order_confirmation.html", {"order": order})

# View User Orders
@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "orders/order_list.html", {"orders": orders})

# View Order Details
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/order_detail.html", {"order": order})

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status != "Cancelled":
        order.status = "Cancelled"
        order.save()
    
    return redirect("track-order", order_id=order.id)

@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/order_details.html", {"order": order})