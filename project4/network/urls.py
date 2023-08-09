
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("create_post", views.create_post, name="create_post"),
    path("users/<int:user_id>", views.view_profile, name="view_profile"),
    path("follow/<int:profile_user_id>", views.follow, name="follow"),
    path("unfollow/<int:profile_user_id>", views.unfollow, name="unfollow"),
]
