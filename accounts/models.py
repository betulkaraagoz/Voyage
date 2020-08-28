from django.contrib.auth.models import User
from django.db import models


# class Owner(models.Model):
#     owner = models.OneToOneField(User, on_delete=models.CASCADE)
#
#     phone = models.TextField(max_length=50)
#
#
# class Customer(models.Model):
#     customer = models.OneToOneField(User, on_delete=models.CASCADE)


class OwnerMail(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner')
    mail = models.CharField(null=True, blank=True, max_length=100)


class UserProfilePhoto(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(null=True, blank=True)

