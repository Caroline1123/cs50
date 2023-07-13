from django.contrib import admin
from .models import User, Listing, Bid, Comment

# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user",'comment', "listing_id", "date_posted")

class ListingAdmin(admin.ModelAdmin):
    ...

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment, CommentAdmin)