from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.contrib import messages
from django.core.paginator import Paginator
from .models import CustomUser, Recipe, LikedRecipe, Cookbook, Exercise
from unslugify import unslugify

def index(request):
    user = request.user
    try:
        liked_recipes_list = LikedRecipe.objects.filter(user=user).values_list('recipe', flat=True)
        liked_recipes = Recipe.objects.filter(id__in=liked_recipes_list)
        cookbook_list = Cookbook.objects.filter(user=user).values_list('recipe', flat=True)
        cookbook_ids = cookbook_list.values_list('recipe__id', flat=True)
        liked_ids = liked_recipes_list.values_list('recipe__id', flat=True)
        cookbook = Recipe.objects.filter(id__in=cookbook_list)
        return render(request, "fitness_app/index.html", {
            "user": user,
            "recipes": liked_recipes,
            'cookbook_ids': cookbook_ids,
            "liked_ids": liked_ids,
            "cookbook": cookbook
        })
    except TypeError:
        return render(request, "fitness_app/index.html")   


def recipes(request):
    recipes = Recipe.objects.all().order_by('-id')
    user = request.user
    paginator = Paginator(recipes, 15)
    start = int(request.GET.get('start', 0))
    data = paginator.get_page(start // 15 + 1)
    try:
        liked_recipes = LikedRecipe.objects.filter(user=user).values_list('recipe', flat=True)
        cookbook = Cookbook.objects.filter(user=user).values_list('recipe', flat=True)
        return render(request, 'fitness_app/recipes.html', {
            'data': data, 
            'start': start,
            'liked_recipes': liked_recipes,
            'cookbook': cookbook
        })
    except TypeError:
        return render(request, 'fitness_app/recipes.html', {
            'data': data, 
            'start': start
        })


def recipe(request, id, title):
    return render(request, "fitness_app/recipe.html", {
        "recipe": Recipe.objects.get(id=id)
    })


def categories(request):
    categories = set()
    recipes = Recipe.objects.all()

    for recipe in recipes:
        categories |= set(recipe.categories)

    categories = sorted(categories)

    # Create a dictionary of categories and their counts
    category_counts = {}
    for category in categories:
        category_count = len(Recipe.objects.filter(categories__icontains=category))
        category_counts[category] = category_count

    return render(request, 'fitness_app/categories.html', {
        'categories': categories,
        'category_counts': category_counts,
    })


def category(request, category):
    user = request.user
    category = unslugify(category)
    recipes = Recipe.objects.filter(categories__icontains=category)

    try:
        liked_recipes = LikedRecipe.objects.filter(user=user).values_list('recipe', flat=True)
        cookbook = Cookbook.objects.filter(user=user).values_list('recipe', flat=True)
        return render(request, 'fitness_app/category.html', {
            'recipes': recipes,
            'category': category,
            'liked_recipes': liked_recipes,
            'cookbook': cookbook
        })
    except TypeError:
        return render(request, 'fitness_app/category.html', {
            'category': category,
            'recipes': recipes
        })


def search(request):
    query = request.GET.get('q')
    category = request.GET.get('search_type')
    if query:
        return redirect('search_results', search_type=category, query=query)
    else:
        return render(request, 'fitness_app/layout.html')


def search_results(request, search_type, query):
    if search_type == 'recipes':
        search_results = Recipe.objects.filter(title__icontains=query)
    # elif search_type == 'exercises':
        # search_results = Exercise.objects.filter(name__icontains=query)
    else:
        search_results = []

    return render(request, 'fitness_app/search.html', {
        'recipes': search_results,
        'query': query,
        'search_type': search_type
        })


@login_required
def like_recipe(request):
    if request.method == 'POST':
        recipe_id = request.POST.get('recipe_id')
        recipe = Recipe.objects.get(id=recipe_id)
        liked_recipe = LikedRecipe(user=request.user, recipe=recipe)
        liked_recipe.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def unlike_recipe(request):
    if request.method == 'POST':
        recipe_id = request.POST.get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        LikedRecipe.objects.filter(user=request.user, recipe=recipe).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def add_to_cookbook(request):
    if request.method == 'POST':
        recipe_id = request.POST.get('recipe_id')
        recipe = Recipe.objects.get(id=recipe_id)
        liked_recipe = Cookbook(user=request.user, recipe=recipe)
        liked_recipe.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def remove_from_cookbook(request):
    if request.method == 'POST':
        recipe_id = request.POST.get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        Cookbook.objects.filter(user=request.user, recipe=recipe).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def validate_password(request):
    if request.method == 'POST':
        password = request.POST.get('input')
        user = request.user
        if check_password(password, user.password):
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'Incorrect password'})
        

@login_required
def update_user(request):
    user = request.user 
    username = request.POST.get('username')
    phoneNumber = request.POST.get('phoneNumber')
    height = request.POST.get('height')
    weight = request.POST.get('weight')

    user.username = username
    user.phone_number = phoneNumber
    user.height = height
    user.weight = weight

    user.save()
    return JsonResponse({'success': True, 'message': 'Profile updated successfully.'})

@login_required
def change_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password != confirm_password:
            return JsonResponse({'success': False, 'message': 'Passwords do not match.'})
        elif len(new_password) < 8:
            return JsonResponse({'success': False, 'message': 'Password should have at least 8 characters.'})
        else:
            user = request.user
            user.set_password(new_password)
            user.save()
            return JsonResponse({'success': True})
        

@login_required
def exercises(request):
    exercises = Exercise.objects.all().order_by('-id')
    return render(request, "fitness_app/exercises.html", {
        "exercises": exercises
    })


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName').capitalize()
        last_name = request.POST.get('lastName').capitalize()
        phone_number = request.POST.get('number')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        profile_picture = request.FILES.get('image')
        date_of_birth = request.POST.get('date')
        height = request.POST.get('height')
        body_weight = request.POST.get('bodyWeight')
        sex = request.POST.get('sex')

        if (first_name or last_name or phone_number or email or date_of_birth or height or body_weight or sex) == "":
            messages.error(request, "Complete all fields before submitting.")
            return redirect('register')
        
        if password != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        try:
            CustomUser.objects.get(username=username)
            messages.error(request, "Username already taken.")
            return redirect('register')
        except CustomUser.DoesNotExist:
            pass

        try:
            CustomUser.objects.get(email=email)
            messages.error(request, "Email address already taken.")
            return redirect('register')
        except CustomUser.DoesNotExist:
            pass

        try:
            CustomUser.objects.get(profile_picture=profile_picture)
            messages.error(request, "Profile picture already taken.")
            return redirect('register')
        except CustomUser.DoesNotExist:
            pass

        try:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            user.phone_number = phone_number
            user.profile_picture = profile_picture
            user.birth_date = date_of_birth
            user.height = height
            user.weight = body_weight
            user.sex = sex
            user.save()
            login(request, user)
            messages.success(request, "You have successfully registered.")
            return redirect('index')
        except ValueError as e:
            messages.error(request, e)
            return redirect('register')

    return render(request, "fitness_app/register.html", {"messages": messages.get_messages(request)})


def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "fitness_app/login.html", {
                "message": "Invalid email and/or password"
            })
    else:
        return render(request, "fitness_app/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
