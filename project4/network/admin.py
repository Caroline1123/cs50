from django.contrib import admin
from .models import User, Post

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display= ("user", "text", "timestamp")


admin.site.register(Post, PostAdmin)