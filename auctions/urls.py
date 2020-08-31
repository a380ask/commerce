from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("changeCategory", views.changeCategory, name="changeCategory"),
    path("createListing", views.createListing, name="createListing"),
    path("view/<int:id>", views.view, name="view"),
    path("view/watchlist/<int:product_id>", views.addWatchlist, name="watchlist"),
    path("view/watch", views.watch, name="watch"),
    path("comments/<int:product_id>", views.comments, name="comments"),
    path("view/winner/<int:product_id>", views.closebid, name="winner"),
    path("view/category/<str:list>", views.cat, name="category")
]
