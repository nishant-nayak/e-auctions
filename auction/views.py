from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment
from .forms import ListingForm

def index(request):
    listings = Listing.objects.filter(active=True)
    return render(request, 'auction/index.html', {
        'listings' : listings
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse(index))
        else:
            return render(request, 'auction/login.html', {
                'message': 'Invalid Username or Password.',
            })
    
    return render(request, 'auction/login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["fname"]
        last_name = request.POST["lname"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        if password != request.POST["confirmation"]:
            return render(request, "auction/register.html", {
                "message": "Passwords must match."
            })
            
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except IntegrityError:
            return render(request, "auction/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    return render(request, "auction/register.html")

@login_required(login_url='login')
def create(request):
    form = ListingForm()

    if request.method == "POST":
        obj = Listing(user=request.user)
        form = ListingForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
    
    return render(request, 'auction/create.html', {
        'form': form
    })
