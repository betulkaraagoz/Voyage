from datetime import timedelta

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Avg
from django.utils import timezone


def next_day():
    return timezone.now() + timezone.timedelta(days=1)


class Hotel(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=100, default=None)
    location_url = models.CharField(max_length=5000, default=None)
    description = models.CharField(max_length=2000, default=None)
    number_of_rooms = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    icon = models.ImageField(upload_to='images/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_avg_rating(self):
        reviews = Review.objects.filter(hotel_id=self.id)

        if reviews is None:
            return 0

        reviews_average = list(reviews.aggregate(Avg('rating')).values())[0]
        return reviews_average

    def get_rating_count_0_2(self):
        reviews = Review.objects.filter(hotel_id=self.id)
        return reviews.filter(rating__lte=2).count()

    def get_rating_count_2_4(self):
        reviews = Review.objects.filter(hotel_id=self.id)
        return reviews.filter(rating__lte=4, rating__gt=2).count()

    def get_rating_count_4_6(self):
        reviews = Review.objects.filter(hotel_id=self.id)
        return reviews.filter(rating__lte=6, rating__gt=4).count()

    def get_rating_count_6_8(self):
        reviews = Review.objects.filter(hotel_id=self.id)
        return reviews.filter(rating__lte=8, rating__gt=6).count()

    def get_rating_count_8_10(self):
        reviews = Review.objects.filter(hotel_id=self.id)
        return reviews.filter(rating__gt=8).count()

    def get_percentage_8_10(self):
        reviews = Review.objects.filter(hotel_id=self.id)

        rate = reviews.filter(rating__gt=8).count()
        if rate != 0:
            return (Review.objects.filter(hotel_id=self.id).count() / rate) * 100
        else:
            return 0

    def get_percentage_6_8(self):
        reviews = Review.objects.filter(hotel_id=self.id)
        rate = reviews.filter(rating__lte=8, rating__gt=6).count()

        if rate != 0:
            return (Review.objects.filter(hotel_id=self.id).count() / rate) * 100
        else:
            return 0

    def get_percentage_4_6(self):
        reviews = Review.objects.filter(hotel_id=self.id)
        rate = reviews.filter(rating__lte=6, rating__gt=4).count()

        if rate != 0:
            return (Review.objects.filter(hotel_id=self.id).count() / rate) * 100
        else:
            return 0

    def get_percentage_2_4(self):
        reviews = Review.objects.filter(hotel_id=self.id)
        rate = reviews.filter(rating__lte=4, rating__gt=2).count()

        if rate != 0:
            return (Review.objects.filter(hotel_id=self.id).count() / rate) * 100
        else:
            return 0

    def get_percentage_0_2(self):
        reviews = Review.objects.filter(hotel_id=self.id)
        rate = reviews.filter(rating__lte=2).count()

        if rate != 0:
            return (Review.objects.filter(hotel_id=self.id).count() / rate) * 100
        else:
            return 0


class AdditionalImages(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)


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
    check_out = models.DateField(default=next_day)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest = models.ForeignKey(User, on_delete=models.CASCADE)


class Review(models.Model):
    customer = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    review = models.CharField(max_length=1000)
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(10)])
    date = models.DateField(default=timezone.now())
