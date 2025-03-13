from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Email")

class UserUpdateForm(forms.ModelForm):
    favorite_pick_up_point = forms.CharField(required=False)
    phone_number = forms.CharField(required=False)
    delivery_address = forms.CharField(required=False)
    home_address = forms.CharField(required=False)
    companies = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            profile.favorite_pick_up_point = self.cleaned_data.get('favorite_pick_up_point', profile.favorite_pick_up_point)
            profile.phone_number = self.cleaned_data.get('phone_number', profile.phone_number)
            profile.delivery_address = self.cleaned_data.get('delivery_address', profile.delivery_address)
            profile.home_address = self.cleaned_data.get('home_address', profile.home_address)
            profile.companies = self.cleaned_data.get('companies', profile.companies)
            profile.save()
        return user


