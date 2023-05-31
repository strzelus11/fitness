from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.contrib import messages
from django.core.paginator import Paginator
from .models import CustomUser, Recipe, LikedRecipe, Cookbook, Exercise, LikedExercise, Training
from unslugify import unslugify
import json

def index(request):
    user = request.user
    try:
        liked_recipes_list = LikedRecipe.objects.filter(user=user).values_list('recipe', flat=True)
        liked_exercises_list = LikedExercise.objects.filter(user=user).values_list('exercise', flat=True)
        liked_recipes = Recipe.objects.filter(id__in=liked_recipes_list)
        liked_exercises = Exercise.objects.filter(id__in=liked_exercises_list)
        cookbook_list = Cookbook.objects.filter(user=user).values_list('recipe', flat=True)
        training = Training.objects.filter(user=user)
        cookbook_ids = cookbook_list
        liked_ids = liked_recipes_list
        liked_exercises_ids = liked_exercises_list
        cookbook = Recipe.objects.filter(id__in=cookbook_list)

        return render(request, "fitness_app/index.html", {
            "user": user,
            "recipes": liked_recipes,
            "exercises": liked_exercises,
            'cookbook_ids': cookbook_ids,
            "liked_ids": liked_ids,
            "liked_exercises_ids": liked_exercises_ids,
            "cookbook": cookbook,
            "training": training
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


def types(request):
    types = set()
    exercises = Exercise.objects.all()

    for exercise in exercises:
        types.add(exercise.type)

    types = sorted(types)

    # Create a dictionary of types and their counts
    type_counts = {}
    for type in types:
        type_count = len(Exercise.objects.filter(type=type))
        type_counts[type] = type_count

    return render(request, 'fitness_app/types.html', {
        'types': types,
        'type_counts': type_counts,
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
    

def type(request, type):
    user = request.user
    type = unslugify(type)
    exercises = Exercise.objects.filter(type__icontains=type)

    try:
        liked_exercises = LikedExercise.objects.filter(user=user).values_list('exercise', flat=True)
        training = Training.objects.filter(user=user).values_list('exercise', flat=True)
        return render(request, 'fitness_app/type.html', {
            'exercises': exercises,
            'type': type,
            'liked_exercises': liked_exercises,
            'training': training
        })
    except TypeError:
        return render(request, 'fitness_app/type.html', {
            'type': type,
            'exercises': exercises
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
    elif search_type == 'exercises':
        search_results = Exercise.objects.filter(name__icontains=query)
    else:
        search_results = []

    return render(request, 'fitness_app/search.html', {
        'data': search_results,
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
    image = request.FILES.get('profileImage')
    username = request.POST.get('username')
    phoneNumber = request.POST.get('phoneNumber')
    height = request.POST.get('height')
    weight = request.POST.get('weight')
    print(image)

    user.username = username
    user.phone_number = phoneNumber
    user.height = height
    user.weight = weight

    if image:
        try:
            user.profile_picture = image
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': str(e)})

    user.save()

    # Return updated user data in the response
    response_data = {
        'success': True,
        'message': 'Profile updated successfully.',
        'user': {
            'username': user.username,
            'phoneNumber': user.phone_number,
            'height': user.height,
            'weight': user.weight,
        }
    }

    return JsonResponse(response_data)

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

            # Redirect to the login page
            return redirect('login')

    return JsonResponse({'success': False, 'message': 'Invalid request.'})
        

def exercises(request):
    exercises = Exercise.objects.all().order_by('-id')
    user = request.user
    try:
        liked_exercises = LikedExercise.objects.filter(user=user).values_list('exercise', flat=True)
        training = Training.objects.filter(user=user).values_list('exercise', flat=True)
        return render(request, 'fitness_app/exercises.html', {
            'liked_exercises': liked_exercises,
            'training': training,
            'exercises': exercises
        })
    except TypeError:
        return render(request, 'fitness_app/exercises.html', {
            'exercises': exercises
        })


def exercise(request, id, name):
    exercise = Exercise.objects.get(id=id)
    return render(request, "fitness_app/exercise.html", {
        "exercise": exercise
    })


def add_exercise(request):
    if request.method == 'POST':
        # Retrieve form data from AJAX request
        data = json.loads(request.body)
        name = data.get('name').title()
        type = data.get('type')
        video_link = data.get('video_link')
        description = data.get('description').splitlines()

        # Perform database update
        exercise = Exercise.objects.create(
            name=name,
            type=type,
            video_link=video_link,
            description=description
        )

        # Return a JSON response indicating success
        response = {
            'status': 'success',
            'message': 'Exercise updated successfully'
        }
        return JsonResponse(response)

    # Return a JSON response indicating an error for unsupported request methods
    response = {
        'status': 'error',
        'message': 'Invalid request method'
    }
    return JsonResponse(response)


def add_recipe(request):
    if request.method == 'POST':
        # Retrieve form data from AJAX request
        data = json.loads(request.body)
        title = data.get('title').title()
        category = data.get('category')
        image_link = data.get('image_link')
        ingredients = data.get('ingredients').splitlines()
        description = data.get('description').splitlines()

        # Perform database update
        recipe = Recipe.objects.create(
            title=title,
            category=category,
            image=image_link,
            ingredients=ingredients,
            description=description
        )

        # Return a JSON response indicating success
        response = {
            'status': 'success',
            'message': 'Exercise updated successfully'
        }
        return JsonResponse(response)

    # Return a JSON response indicating an error for unsupported request methods
    response = {
        'status': 'error',
        'message': 'Invalid request method'
    }
    return JsonResponse(response)


@login_required
def like_exercise(request):
    if request.method == 'POST':
        exercise_id = request.POST.get('exercise_id')
        exercise = Exercise.objects.get(id=exercise_id)
        liked_exercise = LikedExercise(user=request.user, exercise=exercise)
        liked_exercise.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def unlike_exercise(request):
    if request.method == 'POST':
        exercise_id = request.POST.get('exercise_id')
        exercise = get_object_or_404(Exercise, pk=exercise_id)
        LikedExercise.objects.filter(user=request.user, exercise=exercise).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def add_to_training(request):
    if request.method == 'POST':
        exercise_id = request.POST.get('exercise_id')
        exercise = Exercise.objects.get(id=exercise_id)
        liked_recipe = Training(user=request.user, exercise=exercise)
        liked_recipe.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def save_sets_reps(request):
    if request.method == 'POST':
        user = request.user
        exercise_id = request.POST.get('exercise_id')
        sets = request.POST.get('sets')
        reps = request.POST.get('reps')

        # Save the sets and reps in the Exercise model
        exercise = Exercise.objects.get(id=exercise_id)
        training = Training.objects.get(exercise=exercise, user=user)
        training.sets = sets
        training.reps = reps
        training.save()

        return JsonResponse({'message': 'Sets and reps saved successfully.'})

    return JsonResponse({'error': 'Invalid request.'})


@login_required
def remove_from_training(request):
    if request.method == 'POST':
        exercise_id = request.POST.get('exercise_id')
        exercise = get_object_or_404(Exercise, pk=exercise_id)
        Training.objects.filter(user=request.user, exercise=exercise).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


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
