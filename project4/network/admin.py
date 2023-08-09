from django.contrib import admin
from .models import User, Post, Following

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display= ("user", "text", "timestamp")
   

admin.site.register(Post, PostAdmin)
admin.site.register(Following)
admin.site.register(User)