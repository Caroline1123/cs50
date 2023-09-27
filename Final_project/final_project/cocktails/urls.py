from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name = "index"),
    path("login", views.login_view, name = "login"),
    path("logout", views.logout_view, name = "logout"),
    path("register", views.register, name = "register"),
    path("random", views.random, name="random"),
    path("random_recipe", views.random_recipe, name="random_recipe")
]