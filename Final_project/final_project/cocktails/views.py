from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import IntegrityError
import requests

from .models import User


# Create your views here.
def index(request):
    return render(request, "cocktails/index.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "cocktails/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "cocktails/login.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if confirmation != password:
            return render(request, "cocktails/register.html", {
                "message" : "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "cocktails/register.html", {
                "message" : "Username already in use."
            })
        login(request,user)
        return HttpResponseRedirect(reverse("index"))
    
    else:
        return render(request, "cocktails/register.html")
    
def random(request):
    return render(request, "cocktails/random.html")
    
def random_recipe(request):
    response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/random.php')
    if response.status_code == 200 :
        random_recipe = response.json().get('drinks', [])[0]
        ingredients = {}
        for i in range(1, 16):
            ingredient_key = f'strIngredient{i}'
            measure_key = f'strMeasure{i}'
            ingredient = random_recipe.get(ingredient_key)
            measure = random_recipe.get(measure_key)
            if ingredient:
                ingredients[ingredient] = measure
        return render(request, "cocktails/random.html", {
            "random": random_recipe,
            "ingredients": ingredients,
            })
    else :
        # TODO: change error 
        return HttpResponse("Error")