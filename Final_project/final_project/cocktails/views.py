from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
import json
import requests

# Create your views here.
def index(request):
    return render(request, "cocktails/index.html")

def random(request):
    return render(request, "cocktails/random.html")
    
def name_search(request):
    return render(request, "cocktails/search.html")

def ingredient_search(request):
    return render(request, "cocktails/ingredient.html")

def view_results(request):
    if request.method == "POST":
        name = request.POST.get("cocktail_name")
        ingredient = request.POST.get("cocktail_ingredient")
    if not name and not ingredient:
        name = ''
        ingredient = ''
    # fetch results from API
    if ingredient:
        try:
            response = requests.get(f'https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={ingredient}')
            response.raise_for_status()
            results = response.json()
        except (json.decoder.JSONDecodeError, requests.exceptions.RequestException):
            return render(request, "cocktails/results.html", {
                'ingredient': ingredient,
                'results': None,
                })
    else:
        response = requests.get(f'https://www.thecocktaildb.com/api/json/v1/1/search.php?s={name}')
        results = response.json()
     
    results = results["drinks"]

    return render(request, "cocktails/results.html", {
        'ingredient' : ingredient,
        'name' : name, 
        'results' : results,
    })

def recipe(request, cocktail_id):
    results = requests.get(f'https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={cocktail_id}')
    results = results.json()
    recipe = results["drinks"][0]
    ingredients = []
    for i in range(1,16):
        name = recipe.get(f'strIngredient{i}')
        quantity = recipe.get(f'strMeasure{i}')
        if name and quantity:
            ingredients.append([name, quantity])
    return render(request, "cocktails/recipe.html", {
                      "recipe": recipe,
                      "ingredients": ingredients,
                  })

def all_cocktails(request):
    alpha = []
    for i in range(26):
        alpha.append(chr(ord('A')+ i))
    return render(request, "cocktails/all_cocktails.html", {
        "alpha" : alpha,
    })

def letter_find(request, letter):
    response = requests.get(f'https://www.thecocktaildb.com/api/json/v1/1/search.php?f={letter}')
    results = response.json()
    results = results["drinks"]
    alpha = []
    for i in range(26):
        alpha.append(chr(ord('A')+ i))
    return render(request, "cocktails/all_cocktails.html", {
        "alpha" : alpha,
        "results": results,
        "al":letter
    })
