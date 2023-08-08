import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


from .forms import PostForm
from .models import User, Post


def index(request):
    return render(request, "network/index.html", {
        "form" : PostForm()
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
    

@csrf_exempt
@login_required
def create_post(request):
    # Composing a new post must be done via POST
    if request.method == "POST":
        data = json.loads(request.body)
        text = data.get("text", "")
        if text == "":
            return JsonResponse({
                "error": "No text found."
            }, status=400)
        # Create post
        user = request.user
        post = Post(
            user=user,
            text=text,
        )
        post.save()
        return JsonResponse({"message": "Post sent successfully."}, status=201)
    # Show all posts when method is GET
    else : 
        posts = Post.objects.all().order_by("-timestamp").all()
        return JsonResponse([post.serialize() for post in posts], safe=False)


@csrf_exempt
@login_required
def show_user(request, username):
    # Query for requested user
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    # Return user details
    if request.method == "GET":
        user_details = {
            "username": user.username,
            "last_login" : user.last_login,
            "date_joined" : user.date_joined,
        }
        return JsonResponse(user_details)

    # User must be via GET
    else:
        return JsonResponse({
            "error": "GET request required."
        }, status=400)
    