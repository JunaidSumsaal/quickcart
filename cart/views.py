from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from products.models import Product


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()

    subtotal = cart.total_price()
    shipping_fee = Decimal("5.00") if cart_items else Decimal("0.00")
    tax = round(subtotal * Decimal("0.05"), 2)

    total = subtotal + shipping_fee + tax

    return render(request, "cart/cart.html", {
        "cart": cart,
        "cart_items": cart_items,
        "subtotal": subtotal,
        "shipping_fee": shipping_fee,
        "tax": tax,
        "total": total,
    })


@login_required
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    action = request.GET.get("action")

    if action == "increase":
        item.quantity += 1
    elif action == "decrease" and item.quantity > 1:
        item.quantity -= 1
    item.save()

    return redirect("view-cart")


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect("view-cart")


# Add to Cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        cart_item.quantity += 1

    cart_item.save()
    return redirect("view-cart")

# Clear Cart


@login_required
def clear_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    return redirect("view-cart")
