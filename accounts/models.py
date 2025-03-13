from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=20, blank=True)
    home_address = models.TextField(blank=True)
    delivery_address = models.TextField(blank=True)
    favorite_pick_up_point = models.CharField(max_length=200, blank=True)
    companies = models.TextField(blank=True)
    payment_method = models.CharField(max_length=100, blank=True)
    payment_method_expiry = models.CharField(max_length=7, blank=True)  # e.g., '10/2024'

    def __str__(self):
        return f'{self.user.username} Profile'

    # Add methods to calculate order count, reviews count, etc.
    def order_count(self):
        return self.user.orders.count()

    def review_count(self):
        return self.user.reviews.count()

    def favorite_count(self):
        return self.user.favorites.count()

    def product_return_count(self):
        return self.user.product_returns.count()
