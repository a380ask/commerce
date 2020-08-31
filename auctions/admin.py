from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(auctionListing)
admin.site.register(bid)
admin.site.register(category)
admin.site.register(watchList)
admin.site.register(comments_table)
admin.site.register(winner)