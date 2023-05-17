from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipes', views.recipes, name='recipes'),
    path('recipe/<int:id>/<slug:title>', views.recipe, name='recipe'),
    path('categories', views.categories, name='categories'),
    path('recipes/<slug:category>', views.category, name='category'),
    path('search', views.search, name='search'),
    path('search/<str:search_type>/<str:query>', views.search_results, name='search_results'),
    path('like-recipe', views.like_recipe, name='like-recipe'),
    path('unlike-recipe', views.unlike_recipe, name='unlike-recipe'),
    path('check-password', views.validate_password, name='check-password'),
    path('change-password', views.change_password, name='change-password'),
    path('update-user', views.update_user, name='update-user'),
    path('add-to-cookbook', views.add_to_cookbook, name='add-to-cookbook'),
    path('remove-from-cookbook', views.remove_from_cookbook, name='remove-from-cookbook'),

    path('register', views.register, name='register'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout")
]