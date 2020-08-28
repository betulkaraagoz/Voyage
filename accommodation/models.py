from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone


class Hotel(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=100, default=None)
    location_url = models.CharField(max_length=5000, default=None)
    description = models.CharField(max_length=2000, default=None)
    number_of_rooms = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/')
    icon = models.ImageField(upload_to='images/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Room(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    is_reserved = models.BooleanField(default=False)
    number_of_people = models.PositiveIntegerField()
    assoc_hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    check_in = models.DateField(default=timezone.now)
    check_out = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest = models.ForeignKey(User, on_delete=models.CASCADE)


class Review(models.Model):
    customer = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    review = models.CharField(max_length=1000)
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(10)])
    date = models.DateField(default=timezone.now())
