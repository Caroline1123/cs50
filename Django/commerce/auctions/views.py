from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime 


from .models import User, Listing, Bid, Watchlist, Comment


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    if request.method == "POST":
        user = request.user
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.POST["image"]
        price = request.POST["start_price"]
        date_listed = datetime.now()  
        bids_count = 0
        category = request.POST["category"]

        listing = Listing.objects.create(user=user,
            title=title,
            description=description,
            image=image,
            price=price,
            winning_bid=price,
            date_listed=date_listed,
            bids_count=bids_count,
            category=category
        )
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create.html", {
        "categories": Listing.CATEGORIES
    })

def view_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    comments = Comment.objects.filter(listing_id=listing_id)
    if not request.user.is_authenticated:
        return render(request, "auctions/listings.html", {
            "listing":listing,
            "comments":comments,
        })
    watchlist= Watchlist.objects.filter(user=request.user).filter(listings=listing)
    if listing.winning_bid > listing.price:
        bid = Bid.objects.filter(listing_id=listing_id).last()
        return render(request, "auctions/listings.html", {
            "listing":listing,
            "bid":bid,
            "watchlist": watchlist,
            "comments":comments,
        })
    else : 
        return render(request, "auctions/listings.html", {
            "listing":listing,
            "watchlist": watchlist,
            "comments":comments,
        })

@login_required
def bid(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        amount = float(request.POST["amount"])
        if amount > listing.winning_bid:
            # Increase bid counter by one for this listing
            listing.bids_count += 1
            # Update winning_bid value for this listing
            listing.winning_bid = amount
            listing.save()
            bid= Bid.objects.create(user=request.user,
                amount=amount,
                listing_id=listing
                )
            bid.save()
            return render(request, "auctions/listings.html", {
                "listing":listing,
                "bid":bid,
            })
        elif amount <= listing.winning_bid :
            return HttpResponse("Your bid must be higher than the current listed price.")
        
@login_required
def add_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    watchlist = Watchlist.objects.create(user=request.user,
                                        listings=listing)
    watchlist.save()
    return HttpResponseRedirect(reverse("view_listing", args=[listing_id]))
    
@login_required
def remove_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    watchlist = Watchlist.objects.filter(user=request.user).filter(listings=listing)
    watchlist.delete()
    return HttpResponseRedirect(reverse("view_listing", args=[listing_id]))

@login_required
def watchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user)
    listings = Listing.objects.filter(id__in=watchlist.values("listings"))
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

@login_required
def close_auction(request, listing_id):
    Listing.objects.filter(pk = listing_id).update(open=False)
    return HttpResponseRedirect(reverse("index"))

@login_required
def add_comment(request, listing_id):
    if request.method == "POST":
        user = request.user
        listing = Listing.objects.get(pk=listing_id)
        content = request.POST["comment"]
        date_posted = datetime.now()
        comment = Comment.objects.create(user=user,
                                         comment=content,
                                         listing_id=listing,
                                         date_posted=date_posted)
        return redirect("view_listing", listing_id=listing_id)

def view_category(request):
    filter = request.GET.get('category')
    listings = Listing.objects.all()
    categories = Listing.CATEGORIES
    if filter :
        listings = Listing.objects.filter(category=filter)
    else : 
        listings = Listing.objects.all()
    return render(request,"auctions/categories.html", {
        "listings":listings,
        "category":filter,
        "categories" : categories, 
        })


