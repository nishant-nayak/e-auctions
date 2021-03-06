from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing
from .forms import ListingForm

# Default view of the website, this is the first page that the user will see
def index(request):
    # Fetch all active listings to display on the main page
    # SQL : SELECT * FROM listings WHERE acitve=True;
    listings = Listing.objects.filter(active=True)

    # Render the webpage with all active listings as context
    return render(request, 'auction/index.html', {
        'listings' : listings
    })

# Login view of the web application
def login_view(request):
    # If user tried to access this page by submitting the login form
    if request.method == 'POST':
        # Retrieve the username and password from the POST parameters
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user by comparing the username and password to the data available in the database
        # SQL : SELECT * FROM user WHERE username={username} AND password={hash(password)}
        user = authenticate(request, username=username, password=password)

        # If the user exists and the password is valid, login the user and redirect them to the index page
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse(index))
        # If the authenticate function did not return a user, then the input data is invalid
        # Render the login page again with error message
        else:
            return render(request, 'auction/login.html', {
                'message': 'Invalid Username or Password.',
            })
    
    # If the user tried to access this page by clicking the login link
    return render(request, 'auction/login.html')

# Logout view of the web application
def logout_view(request):
    # Logout the user, and redirect them back to the index page
    logout(request)
    return HttpResponseRedirect(reverse('index'))

# Register view of the web application
def register(request):
    # If the user tried to access the page by submitting the register form
    if request.method == "POST":
        # Retrieve the data from the POST parameters
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["fname"]
        last_name = request.POST["lname"]

        # Ensure password matches confirmation
        # TODO: Move this confirmation to the front-end as well using JS
        password = request.POST["password"]
        if password != request.POST["confirmation"]:
            return render(request, "auction/register.html", {
                "message": "Passwords must match."
            })
            
        # Attempt to create new user
        try:
            # SQL : INSERT INTO user VALUES ({username}, {email}, {password}, {first_name}, {last_name}); COMMIT;
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        # If username already exists, Django will throw an integrity error since username must be unique
        except IntegrityError:
            return render(request, "auction/register.html", {
                "message": "Username already taken."
            })
        # The user is created and saved to the database, so login the user and redirect them to the index page
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    # If the user tried to access the page by clicking the register link
    return render(request, "auction/register.html")

# Create view of the web application
# User needs to be logged in to create a new listing
@login_required(login_url='login')
def create(request):
    # Create an instance of the Listing Form
    form = ListingForm()

    # If the user tried to access the page by submitting the create form
    if request.method == "POST":
        # Create a Listing object
        obj = Listing(user=request.user)
        # Fill in the values of the Listing object from the ListingForm
        # SQL : INSERT INTO listing SELECT * FROM ListingForm;
        form = ListingForm(request.POST, instance=obj)
        if form.is_valid():
            # SQL : COMMIT;
            form.save()
            return HttpResponseRedirect(reverse('index'))
    
    # If user tried to access this page by clicking the Create Listing link, render the page with the ListingForm form
    return render(request, 'auction/create.html', {
        'form': form
    })
