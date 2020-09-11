from django.contrib import admin
from blog.models import BlogPost, BlogPostImages
from .models import Hotel, Reservation, Room, Review, AdditionalImages
from accounts.models import CustomerLikes, UserPP

admin.site.register(Hotel)
admin.site.register(Reservation)
admin.site.register(Room)
admin.site.register(Review)
admin.site.register(AdditionalImages)
admin.site.register(CustomerLikes)
admin.site.register(UserPP)
admin.site.register(BlogPost)
admin.site.register(BlogPostImages)
