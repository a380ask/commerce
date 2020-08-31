from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class auctionListing(models.Model):
    productName = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    seller_username = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    image = models.URLField(max_length=300, blank=True, null=True)

class bid(models.Model):
    user = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    list_id = models.IntegerField()
    bid = models.IntegerField()

class category(models.Model):
    category = models.CharField(max_length=100)

class watchList(models.Model):
    user = models.CharField(max_length=100)
    list_id = models.IntegerField()

class comments_table(models.Model):
    user = models.CharField(max_length=100)
    list_id = models.IntegerField()
    comment = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

class winner(models.Model):
    owner = models.CharField(max_length=64)
    winner = models.CharField(max_length=64)
    listingid = models.IntegerField()
    winprice = models.IntegerField()
    title = models.CharField(max_length=64, null=True)

