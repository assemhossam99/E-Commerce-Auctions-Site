from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length = 64)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(max_length = 128)
    description = models.CharField(max_length = 1024)
    startingBid = models.IntegerField()
    currentBid = models.IntegerField(null = True, blank = True)
    imageURL = models.URLField(max_length = 500, null = True, blank = True)
    Category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = "listings", null = True, blank = True)

    def __str__(self):
        return f"{self.id}: {self.title} - {self.startingBid}$ - {self.currentBid}"

class Comment(models.Model):
    commentContent = models.CharField(max_length = 1024)
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "comments")

    def __str__(self):
        return f"Comment {self.id} on Listing {self.Listing.id}: {self.commentContent}"

class Bid(models.Model):
    value = models.IntegerField()
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "bids")

    def __str__(self):
        return f"Bid {self.id} on Listing {self.Listing.id}: {self.value}"