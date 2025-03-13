from django.urls import path
from .views import view_cart, add_to_cart, update_cart_item, remove_from_cart, clear_cart

urlpatterns = [
    path("", view_cart, name="view-cart"),
    path("add/<int:product_id>/", add_to_cart, name="add-to-cart"),
    path("update/<int:item_id>/", update_cart_item, name="update-cart-item"),
    path("remove/<int:item_id>/", remove_from_cart, name="remove-from-cart"),
    path("clear/", clear_cart, name="clear-cart"),
]
