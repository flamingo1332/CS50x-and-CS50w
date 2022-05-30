from datetime import date
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.db.models import DecimalField
from django.core.validators import MaxValueValidator, MinValueValidator 
categories = [('Electronics', 'electronics'), ('Fashion', 'fashion'), ('Furniture', 'furniture'), ('Food', 'food'), ('Toys & Hobby', 'toys & hobby'), ('Other', 'other')]
class User(AbstractUser):
    pass


class Listing(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
	title = models.CharField(max_length=128)
	description = models.TextField()
	starting_bid = models.PositiveIntegerField()
	image = models.ImageField(upload_to="", blank=True)
	category = models.CharField(choices=categories, max_length=30)

	def __str__(self):
		return f"listing_id: {self.id}, title:{self.title}, user_id : {self.user_id}, description:{self.description}, starting_bid: {self.starting_bid}, image: {self.image}, category: {self.category}"


class Bids(models.Model):
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE, default=1)
	username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
	bid = models.DecimalField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], decimal_places=2, max_digits=10)
	date = models.DateTimeField(default=timezone.now)
	closed = models.BooleanField(default=False)

	def __str__(self):
		return f"listing_id:{self.listing.id}, username:{self.username}, bid:{self.bid}, date:{self.date}, closed:{self.closed}"


class Comments(models.Model):
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
	username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
	comment = models.CharField(max_length= 160)
	date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f"username:{self.username}, comment:{self.comment}, date:{self.date}"

class Watchlist(models.Model):
	username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watcher")
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
	def __str__(self):
		return f" listing:{self.listing}, username:{self.username}"


