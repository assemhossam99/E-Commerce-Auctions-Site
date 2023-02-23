from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Listing, Category, Comment, Bid
from django import forms
from .models import User

class NewListingForm(forms.Form):
    title = forms.CharField(label = "Title:", widget=forms.TextInput(attrs={
        'placeholder': 'Title', 
        'style': 'width: 300px;', 
        'class': 'form-control'
        }))
    description = forms.CharField(label = "Description", widget=forms.Textarea(attrs={
        'placeholder': 'Description', 
        'style': 'width: 500px;', 
        'class': 'form-control'
        }))
    startingBid = forms.IntegerField(label = "Starting Bid", min_value = 1, widget=forms.NumberInput(attrs={
        'style': 'width: 100px;', 
        'class': 'form-control'
        }))
    image = forms.CharField(required = False, label = "image", widget=forms.TextInput(attrs={
        'placeholder': 'Image URL', 
        'style': 'width: 300px;', 
        'class': 'form-control'
        }))
    categoryList = [(category.pk, category) for category in Category.objects.all()]
    category = forms.ChoiceField(required = False, choices = ( [('', '')] + [(category.pk, category) for category in Category.objects.all()]), widget=forms.Select(attrs={
        'placeholder': 'Description', 
        'style': 'width: 300px;', 
        'class': 'form-control'
        }))

def index(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            startingBid = form.cleaned_data["startingBid"]
            image = form.cleaned_data["image"]
            category = None
            if form.cleaned_data["category"] != '':
                tmp = form.cleaned_data["category"]
                category = Category.objects.get(id = form.cleaned_data["category"])
            user = request.user
        listing = Listing.objects.create(title = title, description = description, startingBid = startingBid, imageURL = image, category = category, owner = user)
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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

# @login_required
def newListing(request):
    if not request.user.is_authenticated:
        return render(request, "auctions/login.html", {
            "message": "please log in to add new listing"
        })
    else:
        return render(request, "auctions/newListing.html", {
            "form": NewListingForm()
        })

def listing(request, listing_id):
    return render(request, "auctions\listing.html")