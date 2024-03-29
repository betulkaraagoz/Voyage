from django.contrib.auth.models import User
from django.db import models


class OwnerMail(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner')
    mail = models.CharField(null=True, blank=True, max_length=100)


class CustomerLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_hotel = models.ForeignKey("accommodation.Hotel", on_delete=models.CASCADE)


class BlogLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_blog = models.ForeignKey("blog.BlogPost", on_delete=models.CASCADE)


class UserPP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='images/', blank=True, null=True, default=None)
