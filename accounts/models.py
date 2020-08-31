from django.contrib.auth.models import User
from django.db import models


class OwnerMail(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner')
    mail = models.CharField(null=True, blank=True, max_length=100)

