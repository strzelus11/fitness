from django.contrib import admin
from .models import CustomUser, Recipe, LikedRecipe, Cookbook, Exercise, LikedExercise, Training

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Recipe)
admin.site.register(LikedRecipe)
admin.site.register(Cookbook)
admin.site.register(Exercise)
admin.site.register(LikedExercise)
admin.site.register(Training)