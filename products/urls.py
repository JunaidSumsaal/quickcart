from django.urls import path
from .views import (
    add_review, add_to_wishlist, product_list, product_detail, create_product, storefront,
    update_product, delete_product
)

urlpatterns = [
    path("", product_list, name="product-list"),
    path("<int:product_id>/", product_detail, name="product-detail"),
    path("add/", create_product, name="create-product"),
    path("edit/<int:product_id>/", update_product, name="update-product"),
    path("delete/<int:product_id>/", delete_product, name="delete-product"),
    path("", storefront, name="storefront"),
    path('wishlist/add/<int:product_id>/', add_to_wishlist, name='wishlist-add'),
    path('<int:product_id>/add-review/', add_review, name='add-review'),
]
