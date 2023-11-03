from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name = "index"),

    path("random", views.random, name="random"),
    path("search", views.name_search, name="search"),
    path("all", views.all_cocktails, name="all"),
    path("ingredient", views.ingredient_search, name="ingredient"),
    path("view_results", views.view_results, name="results"),
    path("recipe/<int:cocktail_id>", views.recipe, name="recipe"),
    path("letter/<str:letter>", views.letter_find, name="letter"),
]