from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    CATEGORIES = [
        ('ARTS','Art & Collectibles'),
        ('FOOD','Food & Beverages'), 
        ('DYI','DYI'), 
        ('GAME','Games & entertainment'), 
        ('HOME','Home'), 
        ('CLOTH','Clothing'), 
        ('MISC','Miscellaneous'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    image = models.ImageField(blank=True)
    price = models.FloatField()
    winning_bid = models.FloatField()
    date_listed = models.DateTimeField()
    bids_count = models.IntegerField(blank=True)
    open = models.BooleanField(default=True)
    category = models.CharField(max_length=30, blank=True, choices=CATEGORIES)

        
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment= models.CharField(max_length=500)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    date_posted = models.DateTimeField()

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listings = models.ForeignKey(Listing, on_delete=models.CASCADE)