from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Email")

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["username", "email", "avatar"]
