from django.shortcuts import render, HttpResponse, redirect
from posts.models import Post
from posts.forms import PostForm


def homepage_view(request):
    return render(request, "base.html")

def post_list_view(request):
    if request.method == "GET":
        posts = Post.objects.all()
        return render(request, "posts/post_list.html", context={"posts": posts})

def post_detail_view(request, post_id):
    if request.method == "GET":
        post = Post.objects.filter(id=post_id).first()
        return render(request, "posts/post_detail.html", context = {"post": post})
    
def post_create_view(request):
    if request.method == "GET":
        form = PostForm()
        return render(request, "posts/post_create.html", context={"form": form})
    elif request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, "posts/post_create.html", context={"form": form})
        elif form.is_valid():
            data = form.cleaned_data
            post = Post.objects.create(**data)
            return redirect("/posts/")
