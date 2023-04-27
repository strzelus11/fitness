from django.contrib import admin
from .models import CustomUser, Recipe

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Recipe)