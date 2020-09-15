from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from accounts.models import BlogLikes


class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default=None)
    place = models.CharField(max_length=100, default=None)
    continent = models.CharField(max_length=100, default=None)
    post_part_1 = models.CharField(max_length=5000, default=None, null=True)
    subtitle = models.CharField(max_length=200, default=None, null=True, blank=True)
    post_part_2 = models.CharField(max_length=5000, default=None, null=True)
    date = models.DateField(default=timezone.now())
    cover_image = models.ImageField(upload_to='images/', default=None, null=True)
    video_url = models.CharField(max_length=1000, null=True, blank=True)

    def get_short_post(self):
        return self.post_part_1[:500]

    def get_likes_no(self):
        likes_number = BlogLikes.objects.filter(liked_blog=self).count()
        return likes_number


class BlogPostImages(models.Model):
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

