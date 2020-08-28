from django.contrib import admin

from .models import Hotel, Reservation, Room, Review
from accounts.models import OwnerMail

admin.site.register(Hotel)
admin.site.register(Reservation)
admin.site.register(Room)
admin.site.register(OwnerMail)
admin.site.register(Review)
# admin.site.register(Owner)