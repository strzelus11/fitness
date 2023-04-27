from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20)
    birth_date = models.DateField(null=True, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    sex = models.CharField(max_length=6, null=True, blank=True)


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField(max_length=200)
    ingredients = models.JSONField(default=dict)
    recipe = models.JSONField(default=dict)
    categories = models.JSONField(default=dict)

    def __str__(self):
        return self.title
