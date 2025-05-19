from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from users.forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout


def register_view (request):
    if request.method == "GET":
        form = RegisterForm()
        return render(request, "users/register.html", context={"form": form})
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, "users/register.html", context={"form": form})
        elif form.is_valid():
            data = form.cleaned_data
            data.__delitem__("password_confirm")
            User.objects.create_user(**data)
        return redirect("/")

def login_view(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "users/login.html", context= {"form": form})
    if request.method == "POST":
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request, "users/login.html", context = {"form": form})
        elif form.is_valid():
            user = authenticate(request=request, **form.cleaned_data)
            if not user:
                form.add_error(None, "Invalid username or password")
                return render(request, "users/login.html", context = {"form": form})
            elif user:
                login(request, user)
                return redirect("/")