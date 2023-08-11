import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import User, Post, Following
from .forms import PostForm


def index(request):
    # Retrieve all posts and order them by date
    posts = Post.objects.all().order_by("-timestamp").all()
    # Show 10 posts per page
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "form": PostForm,
        "page_obj" : page_obj,
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

@login_required
def create_post(request):
    if request.method == "POST":
        text = request.POST["text"]
        # Check that the post is not an empty string
        if text == "":
            # TO CHANGE :
            return HttpResponse("Cannot create an empty post!")
        # Create new post object
        user = request.user
        post = Post(
            user=user,
            text=text
        )
        post.save()
    return HttpResponseRedirect(reverse("index"))


def view_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    following = Following.objects.filter(user=user_id).count()
    followers = Following.objects.filter(followed_users=user_id).count()
    try:
        follow = Following.objects.get(user=request.user, followed_users=user)
        is_following = True
    except Following.DoesNotExist:
        is_following = False
    user_posts = Post.objects.filter(user=user).order_by("-timestamp").all()
    paginator = Paginator(user_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/users.html", {
        "profile_user": user,
        "page_obj": page_obj,
        "following": following,
        "followers": followers,
        "is_following": is_following
    })

@login_required
def follow(request, user_id):
    profile_user = User.objects.get(pk=user_id)
    follow = Following(
        user=request.user,
        followed_users=profile_user
    )
    follow.save()
    return HttpResponseRedirect(reverse("view_profile", args=[user_id]))

@login_required
def unfollow(request, user_id):
    profile_user = User.objects.get(pk=user_id)
    follow = Following.objects.filter(user=request.user, followed_users=profile_user)
    follow.delete()
    return HttpResponseRedirect(reverse("view_profile", args=[user_id]))

@login_required
def following(request):
    followed_users = Following.objects.filter(user=request.user).values_list('followed_users', flat=True)
    posts = Post.objects.filter(user__in=followed_users).order_by("-timestamp")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "page_obj":page_obj,
        "form":PostForm,
    })

@login_required
def edit(request, post_id):
    if request.method == "POST":
        
        new_text = request.POST["text"]
        post = Post.objects.get(pk = post_id).update(text = new_text)
