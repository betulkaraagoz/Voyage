from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    place = models.CharField(max_length=100)
    post = models.CharField(max_length=5000)
    date = models.DateField(default=timezone.now())
    cover_image = models.ImageField(upload_to='images/', blank=True, null=True)


class BlogPostImages(models.Model):
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

