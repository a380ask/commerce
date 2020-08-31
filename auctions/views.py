from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime

from .models import User, auctionListing, category, watchList, comments_table, winner, bid


def index(request):
    return render(request, "auctions/index.html", {
        "listing": auctionListing.objects.all()
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='/login')
def changeCategory(request):
    if request.method == "POST":
        c = category()
        c.category = request.POST.get('category')
        c.save()
        return render(request, "auctions/category.html", {
            "totalCategory": category.objects.all(),
            "message": "Success!"
        })
    else:
        return render(request, "auctions/category.html",{
            "totalCategory": category.objects.all()
        })

@login_required(login_url='/login')
def createListing(request):
    a = auctionListing()
    if request.method == "POST":
        a.productName = request.POST.get('productName')
        a.category = request.POST.get('category')
        a.seller_username = request.user.username
        a.description = request.POST.get('description')
        a.starting_bid = request.POST.get('starting_bid')
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        a.date = dt_string
        a.image = request.POST.get('image')
        a.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "auctions/createListing.html", {
            "category": category.objects.all()
        })

@login_required(login_url='/login')
def view(request, id):
    if request.method == "GET":
        list_id = auctionListing.objects.get(pk=id)
        added = watchList.objects.filter(list_id=id, user=request.user.username)
        win = winner.objects.filter(listingid=id)
        if win:
            closed = True
        else:
            closed = False
        return render(request, "auctions/viewListing.html", {
            "listing": auctionListing.objects.all(),
            "list_id": list_id,
            "added": added,
            "comment": comments_table.objects.all(),
            "closed": closed,
            "winner": winner.objects.filter(listingid=id)
        })
    else:
        a = auctionListing.objects.get(pk=id)
        rebid = int(request.POST.get('rebid'))
        if (rebid == a.starting_bid or rebid < a.starting_bid):
            return render(request, "auctions/viewListing.html", {
                "listing": auctionListing.objects.all(),
                "list_id": auctionListing.objects.get(pk=id),
                "message": "Your bid should be higher!!",
                "comment": comments_table.objects.all(),
                "winner": winner.objects.filter(listingid=id),
            })
        else:
            a.starting_bid = request.POST.get('rebid')
            a.save()
            bobj = bid.objects.filter(list_id=id)
            if bobj:
                bobj.delete()
            b = bid()
            b.bid = request.POST.get('rebid')
            b.user = request.user.username
            b.title = a.productName
            b.list_id = a.id
            b.save()
            win = winner.objects.filter(listingid=id)
            if win:
                closed = True
            else:
                closed = False
            return render(request, "auctions/viewListing.html", {
                "listing": auctionListing.objects.all(),
                "list_id": auctionListing.objects.get(pk=id),
                "message": "Success!!",
                "comment": comments_table.objects.all(),
                "winner": winner.objects.filter(listingid=id),
                "closed": closed
            })


# Adding something to the WatchList does not work. You will have to play with the function below. Everthing else seems okay.
@login_required(login_url='/login')
def addWatchlist(request, product_id):
    obj = watchList.objects.filter(list_id=product_id, user=request.user.username)
    # checking if it is already added to the watchlist
    if obj:
        # if its already there then user wants to remove it from watchlist
        obj.delete()
        # returning the updated content
        product = auctionListing.objects.filter(id=product_id)
        added = watchList.objects.filter(list_id=product_id, user=request.user.username)
        comment = comments_table.objects.filter(list_id=product_id)
        win = winner.objects.filter(listingid=product_id)
        if win:
            closed = True
        else:
            closed = False
        return render(request, "auctions/viewListing.html", {
            "listing": product,
            "list_id": auctionListing.objects.get(pk=product_id),
            "added": added,
            "comment":comment,
            "message": "removed from watchlist",
            "winner": winner.objects.filter(listingid=product_id),
            "closed": closed
        })
    else:
        obj = watchList()
        obj.user = request.user.username
        obj.list_id = product_id
        obj.save()
        print(obj)
        # returning the updated content
        product = auctionListing.objects.filter(id=product_id)
        added = watchList.objects.filter(list_id=product_id, user=request.user.username)
        comment = comments_table.objects.filter(list_id=product_id)
        win = winner.objects.filter(listingid=product_id)
        if win:
            closed = True
        else:
            closed = False
        return render(request, "auctions/viewListing.html", {
            "listing": product,
            "message": "added to watchlist",
            "added": added,
            "comment": comment,
            "winner": winner.objects.filter(listingid=product_id),
            "list_id": auctionListing.objects.get(pk=product_id),
            "closed": closed
        })

@login_required(login_url='/login')
def watch(request):
    watch = watchList.objects.all()
    return render(request, "auctions/watch.html", {
        "watch": watch,
        "listing": auctionListing.objects.all()
    })

@login_required(login_url='/login')
def comments(request, product_id):
    c = comments_table()
    if request.method == "POST":
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        c.time = dt_string
        c.comment = request.POST.get('comments')
        c.user = request.user.username
        c.list_id = product_id
        c.save()
        product = auctionListing.objects.filter(id=product_id)
        added = watchList.objects.filter(list_id=product_id, user=request.user.username)
        comment = comments_table.objects.filter(list_id=product_id)
        win = winner.objects.filter(listingid=product_id)
        if win:
            closed = True
        else:
            closed = False
        return render(request, "auctions/viewListing.html", {
            "listing": product,
            "message": "added to watchlist",
            "added": added,
            "comment": comment,
            "list_id": auctionListing.objects.get(pk=product_id),
            "winner": winner.objects.filter(listingid=product_id),
            "closed": closed
        })
    else:
        product = auctionListing.objects.filter(id=product_id)
        added = watchList.objects.filter(list_id=product_id, user=request.user.username)
        comment = comments_table.objects.filter(list_id=product_id)
        win = winner.objects.filter(listingid=product_id)
        if win:
            closed = True
        else:
            closed = False
        return render(request, "auctions/viewListing.html", {
            "listing": product,
            "message": "added to watchlist",
            "added": added,
            "comment": comment,
            "list_id": auctionListing.objects.get(pk=product_id),
            "winner": winner.objects.filter(listingid=product_id),
            "closed": closed
        })

@login_required(login_url='/login')
def closebid(request, product_id):
    try:
        b = bid.objects.get(list_id=product_id)
        w = winner()
        list = auctionListing.objects.filter(id=product_id)
        w.owner = request.user.username
        w.winner = b.user
        print(w.winner)
        w.winprice = b.bid
        w.listingid = product_id
        w.title = b.title
        if watchList.objects.filter(list_id=product_id):
            watchobj = watchList.objects.filter(list_id=product_id)
            watchobj.delete()
        if comments_table.objects.filter(list_id=product_id):
            commentobj = comments_table.objects.filter(list_id=product_id)
            commentobj.delete()
        w.save()
        b.delete()
        closed = True
        message = "Successfully closed the bid"
    except:
        message = "There were no bidders. So, the bid has not been closed."
        closed = False
    return render(request, "auctions/winner.html", {
        "winner": winner.objects.filter(listingid=product_id),
        "message": message,
        "closed": closed
    })

@login_required(login_url='/login')
def cat(request, list):
    cate = category.objects.filter(category=list)
    print(cate)
    for i in cate:
        a = auctionListing.objects.filter(category=i.category)
    return render(request, "auctions/specificCat.html",{
        "name":request.user.username,
        "cate":cate,
        "a": a
    })