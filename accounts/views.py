from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm

User = get_user_model()

# Register User
def register_user(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserRegisterForm()
    return render(request, "accounts/register.html", {"form": form})

# Login User
def login_user(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = UserLoginForm()
    return render(request, "accounts/login.html", {"form": form})

# Logout User
@login_required
def logout_user(request):
    logout(request)
    return redirect("login")

# User Profile
@login_required
def profile(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, "accounts/profile.html", {"form": form})

# Password Reset Request
def request_password_reset(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = get_object_or_404(User, email=email)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_url = f"http://127.0.0.1:8000/reset-password/{uid}/{token}/"
        send_mail(
            "Password Reset Request",
            f"Click the link to reset your password: {reset_url}",
            "no-reply@quickcart.com",
            [user.email],
            fail_silently=False,
        )
        return redirect("password_reset_done")

    return render(request, "accounts/password_reset.html")

# Password Reset Confirm
def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if request.method == "POST":
            new_password = request.POST.get("password")
            user.set_password(new_password)
            user.save()
            return redirect("login")

        return render(request, "accounts/password_reset_confirm.html", {"valid": True})
    except:
        return render(request, "accounts/password_reset_confirm.html", {"valid": False})

# Change Password (For logged-in users)
@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "accounts/change_password.html", {"form": form})
