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

    path('register', views.register, name='register'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout")
]