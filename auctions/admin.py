from django.contrib import admin
from .models import Listing, Category, Comment, Bid, WatchList

# Register your models here.

admin.site.register(Listing)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(WatchList)