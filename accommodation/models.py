from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Avg
from django.utils import timezone

from accounts.models import CustomerLikes


def next_day():
    return timezone.now() + timezone.timedelta(days=1)


class Hotel(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=100, default=None)
    location_url = models.CharField(max_length=5000, default=None)
    description = models.CharField(max_length=2000, default=None, null=True, blank=True)
    number_of_rooms = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    icon = models.ImageField(upload_to='images/', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    maps_url = models.CharField(max_length=2000, default=None, null=True, blank=True)
    type = models.CharField(max_length=100, default=None, null=True, blank=True)
    telephone = models.CharField(max_length=100, default=None, null=True, blank=True)
    email = models.EmailField(max_length=200, default=None, null=True, blank=True)
    hotel_website = models.CharField(max_length=1000, default=None, null=True, blank=True)
    number_of_stars = models.IntegerField(default=5)
    standard_price = models.IntegerField(default=1000, blank=True, null=True)

    def get_short_desc(self):
        return self.description[:150]

    def get_reviews_count(self):
        return Review.objects.filter(hotel_id=self.id).count()

    def get_avg_rating(self):
        reviews = Review.objects.filter(hotel_id=self.id)

        if reviews.count() == 0:
            return 0

        reviews_average = list(reviews.aggregate(Avg('rating')).values())[0]
        return reviews_average

    def get_ratings(self):
        reviews = Review.objects.filter(hotel_id=self.id)

        ratings = [reviews.filter(rating__lte=2).count(), reviews.filter(rating__lte=4, rating__gt=2).count(),
                   reviews.filter(rating__lte=6, rating__gt=4).count(), reviews.filter(rating__lte=8, rating__gt=6).count(),
                   reviews.filter(rating__gt=8).count()]

        return ratings

    def get_percentages(self):
        per_1 = (self.get_reviews_count() / self.get_ratings()[0])*100 if self.get_ratings()[0] != 0 else 0
        per_2 = (self.get_reviews_count() / self.get_ratings()[1])*100 if self.get_ratings()[1] != 0 else 0
        per_3 = (self.get_reviews_count() / self.get_ratings()[2])*100 if self.get_ratings()[2] != 0 else 0
        per_4 = (self.get_reviews_count() / self.get_ratings()[3])*100 if self.get_ratings()[3] != 0 else 0
        per_5 = (self.get_reviews_count() / self.get_ratings()[4])*100 if self.get_ratings()[4] != 0 else 0

        percentages = [per_1, per_2, per_3, per_4, per_5]
        return percentages

    def get_popularity(self):
        pop_reservations = Reservation.objects.filter(room__assoc_hotel=self).count()
        pop_likes = CustomerLikes.objects.filter(liked_hotel=self).count()

        return pop_likes + pop_reservations

    def get_reviews_count(self):
        return Review.objects.filter(hotel=self).count()


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

    def days(self):
        return self.check_out.day - self.check_in.day


class Review(models.Model):
    customer = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    review = models.CharField(max_length=1000)
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(10)])
    date = models.DateField(default=timezone.now())

    def get_short_review(self):
        return self.review[:100]
