from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Wishlist(models.Model):
    pass

class Comment(models.Model):
    pass