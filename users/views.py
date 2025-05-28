from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from users.forms import RegisterForm, LoginForm
from users.models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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
            age = data.pop("age", None)
            image = data.pop("image", None)
            user = User.objects.create_user(**data)
            if user:
                Profile.objects.create(user=user, age=age, image=image)
                login(request, user)
                return redirect("/")

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

@login_required(login_url="/login/")
def logout_view(request):
    logout(request)
    return redirect ("/")

@login_required(login_url="/login/")
def profile_view(request):
    user = request.user
    posts = user.posts.all()
    return render(request, "users/profile.html", context={"user":user, "posts":posts})
