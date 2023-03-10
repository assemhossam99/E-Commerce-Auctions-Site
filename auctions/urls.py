from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newListing", views.newListing, name="newListing"),
    path("categories", views.categories, name="categories"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("category/<int:category_id>", views.category, name="category"),
    path("watchlist/<int:user_id>", views.watchlist, name="watchlist")
]
