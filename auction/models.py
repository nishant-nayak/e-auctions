from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator

# Model definition for Listing
class Listing(models.Model):
    # Set of possible categories for a listing
    categories = [
        ('books','Books'),
        ('clothing','Clothing'),
        ('electronics','Electronics'),
        ('home','Home'),
        ('pets','Pet Supplies'),
        ('sports','Sports'),
        ('toys','Toys'),
        ('antiques','Antiques'),
        ('computers','Computers & Networking')
    ]

    # Model attributes
    title = models.CharField(max_length=64)
    desc = models.TextField(max_length=200)
    price = models.FloatField(validators=[MinValueValidator(0, message="Ensure that the starting bid is greater than 0.")])
    image = models.URLField(blank=True)
    category = models.CharField(max_length=20, choices=categories, blank=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    start = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

# Model definition for User, which inherits from AbstractUser
class User(AbstractUser):
    watchlist = models.ManyToManyField(Listing, related_name="watchlist")