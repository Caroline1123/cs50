from django.contrib import admin
from .models import User, Listing, Bid, Comment

# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user",'comment', "listing_id", "date_posted")

class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'winning_bid', 'bids_count','category', 'open', )

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")

class BidAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "listing_id")

admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)