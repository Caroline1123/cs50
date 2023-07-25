from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.show_entry, name="show_entry"),
    path('search/', views.search, name='search'),
    path('create/', views.create, name='create'),
    path('edit/<str:title>', views.edit, name='edit'),
    path('random/', views.random, name="random"),
    path('error/', views.error, name="error"),
    ]