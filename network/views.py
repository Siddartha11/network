from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Post
from .models import User
from .models import Following


def index(request):
    if request.method=="POST":
        post=Post()
        post.owner=request.user
        post.text=request.POST["tweet"]
        post.likes=0
        post.dislikes=0
        post.save()
    all_posts = Post.objects.order_by('-created_at')
    return render(request, "network/index.html",{
        "all_posts":all_posts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request,username):
    user=User.objects.get(username=username)
    crnt_user=request.user
    following_count=user.following.count()
    followers_count=user.followers.count()
    all_user_posts = Post.objects.filter(owner=user).order_by('-created_at')
    is_following=user.followers.filter(following_user_id=crnt_user).exists()
    return render(request, "network/profilepage.html",{
        "user":user,
        "following_count":following_count,
        "followers_count":followers_count,
        "all_posts":all_user_posts,
        "is_following":is_following
    })

