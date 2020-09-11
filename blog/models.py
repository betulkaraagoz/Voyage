from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    place = models.CharField(max_length=100)
    post_part_1 = models.CharField(max_length=5000, default=None, blank=True, null=True)
    subtitle = models.CharField(max_length=200, default=None, blank=True, null=True)
    post_part_2 = models.CharField(max_length=5000, default=None, blank=True, null=True)
    date = models.DateField(default=timezone.now())
    cover_image = models.ImageField(upload_to='images/', blank=True, null=True)
    video_url = models.CharField(max_length=1000, blank=True, null=True)

    def get_short_post(self):
        return self.post_part_1[:500]


class BlogPostImages(models.Model):
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

