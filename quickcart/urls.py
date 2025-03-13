from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from products.views import add_to_wishlist, storefront

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('payments/', include('payments.urls')),
    path("", storefront, name="home"),
    path('wishlist/add/<int:product_id>/', add_to_wishlist, name='wishlist-add'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)