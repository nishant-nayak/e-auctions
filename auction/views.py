from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment
from .forms import ListingForm, BidForm, CommentForm

from datetime import datetime, timezone
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

# Listing view of the web application, takes num as an added argument since each listing has its own page
def listing(request, num):
    # Creating the form instances for Bids and Comments
    bid_form = BidForm()
    comment_form = CommentForm()

    # Creating model instances for Listings, Users and Comments
    try:
        # SQL : SELECT * FROM listing WHERE id={num};
        item = Listing.objects.get(pk=num)
    except:
        # If the given listing number does not exist, render a 404 page
        return render(request, 'auction/404.html')
    
    try:
        # SQL : SELECT * FROM user WHERE id = {request.user.id};
        user = User.objects.get(pk=request.user.id)
    except:
        # If the current user is not signed in, set user to None
        user = None
    
    # SQL : SELECT COUNT(*) FROM bid WHERE item={item};
    bids = Bid.objects.filter(item=item).count()

    # SQL : SELECT * FROM comment WHERE item={item} ORDER BY time DESC;
    comments = Comment.objects.filter(item=item).order_by('time').reverse()
    
    # Initializing variables for checking if the current user is the latest bidder
    bidder = False
    if bids > 0:
        # SQL : SELECT * FROM bid WHERE item={item} ORDER BY time DESC LIMIT 1;
        current_bid = Bid.objects.filter(item=item).order_by('time').last()
        # If the user is logged in, set bidder to True if the current user is also the latest bidder
        if request.user.is_authenticated:
            bidder = current_bid.user == request.user
        
    
    # Calculating the time since the listing was posted
    now = datetime.now(timezone.utc)
    diff = now - item.start
    listing_time = {
        'days': diff.days,
        'hours': (diff.seconds % 86400) // 3600,
        'mins': (diff.seconds % 3600) // 60
    }
    
    # Checking if an item was bought, and the user who bought it
    winner = None
    if not item.active and bids > 0:
        winner = current_bid.user

    # If the user tried to access the page by submitting one of the forms on the page
    if request.method == 'POST':
        
        # Form response from closing listing
        if 'close' in request.POST:
            # Close the listing by updating the active field to False
            # SQL : UPDATE listing SET active=False WHERE id={num};
            item.active = False
            item.save()
            return HttpResponseRedirect(reverse('listing', args=[num]))

        # Form response from placing a bid
        elif 'bid' in request.POST:
            # Fill in the values from the BidForm into the Bid object
            # SQL : INSERT INTO bid SELECT * FROM BidForm;
            obj = Bid(user=user, item=item)
            bid_form = BidForm(request.POST, instance=obj)
            # Check if the input is valid and if so, commit the changes to the database
            if bid_form.is_valid():
                item.price = bid_form.instance.amount
                # SQL : COMMIT;
                item.save()
                bid_form.save()
                return HttpResponseRedirect(reverse('listing', args=[num]))

        # Form response for adding to watchlist
        elif 'watchlist_add' in request.POST:
            # SQL : INSERT INTO watchlist VALUES ({user}, {item}); COMMIT;
            user.watchlist.add(item)
            user.save()
            return HttpResponseRedirect(reverse('listing', args=[num]))

        # Form response for removing from watchlist
        elif 'watchlist_remove' in request.POST:
            # SQL : DELETE FROM watchlist WHERE item={item} AND user={user}; COMMIT;
            user.watchlist.remove(item)
            user.save()
            return HttpResponseRedirect(reverse('listing', args=[num]))
        
        # Form response for adding a comment
        elif 'add_comment' in request.POST:
            obj = Comment(user=user, item=item)
            # SQL : INSERT INTO comment SELECT * FROM CommentForm;
            comment_form = CommentForm(request.POST, instance=obj)
            if comment_form.is_valid():
                # SQL : COMMIT;
                comment_form.save()
                return HttpResponseRedirect(reverse('listing', args=[num]))

    # If the user tried to access the page by clicking the listing link, render the webpage with all the given context
    return render(request, 'auction/listing.html', {
        'item': item,
        'bid_form': bid_form,
        'bids': bids,
        'current_bid': bidder,
        'listing_time': listing_time,
        'winner': winner,
        'wlist': item in user.watchlist.all() if request.user.is_authenticated else None,
        'comment_form': comment_form,
        'comments': comments
    })

# Watchlist view of the web application, shows the watchlist for a particular user so they must be logged in
@login_required(login_url='login')
def watchlist(request):
    # SQL : SELECT * FROM watchlist WHERE user=(SELECT * FROM user WHERE id={request.user.id});
    user = User.objects.get(pk=request.user.id)
    wlist = user.watchlist.all()
    return render(request, 'auction/watchlist.html', {
        'wlist': wlist
    })

# Category view of the web application, shows the listings for each category
def category(request, title):
    categories = Listing.categories
    flag = False
    # Check if the requested category is valid
    for category in categories:
        if title in category:
            flag = True
            break
    
    # If category is not valid, render a 404 page
    if not flag and title != 'index':
        return render(request, 'auction/404.html')
    
    # If the category is index, render the list of categories
    if title == 'index':
        return render(request, 'auction/category.html', {
            'categories': categories,
            'idx': True,
        })
    # If the category is a specific category, render all listings in that category
    else:
        listings = Listing.objects.filter(category=title).filter(active=True)
        return render(request, 'auction/category.html', {
            'listings': listings,
            'idx': False,
        })

# Userpage view of the web application, shows the activity of a specific user
def userpage(request, name):
    try:
        # SQL : SELECT * FROM user WHERE username={name};
        user = User.objects.get(username=name)
    except:
        # If user is not found, render a 404 page
        return render(request, 'auction/404.html')
    
    # SQL : SELECT * FROM listing WHERE user={user};
    items = Listing.objects.filter(user=user)
    # SQL : SELECT * FROM comment WHERE user={user} ORDER BY time DESC;
    comments = Comment.objects.filter(user=user).order_by('time').reverse()

    return render(request, 'auction/userpage.html', {
        'userpage': user,
        'items': items,
        'comments': comments
    })