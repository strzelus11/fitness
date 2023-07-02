## Distinctiveness and Complexity

I believe my project satisfies the distinctiveness and complexity requirements, because I've tried my best to make my project versatile. This is a fitness app, where you have your own account with your personal data such as: birth date, height, weight, etc. You can change some of them, as you go further in your fitness journey. 
The app is basically divided into three sort of "sub-sites": 
- Profile
  - This one containes your liked/saved recipes and exercises and your personal data
- Recipes
  - This one contains all of the recipes 
- Exercises
  - This one contains all of the exercises

Some of the arguments that in my opinion prove fulfillment of the requirements:
- ability to like/unlike, save/unsave recipes and exercises,
- ability to add your own recipes/exercises to database,
- nice user experience ahcieved by using javascript in most of the cases,
- profile, which has "double navigation" which remembers state after the reload,
- search bar with ability to choose whether you search for exercises or recipes
- nice, clean look overall with small animations and small changes that matters in the bigger picture, such as dynamic counts of liked/saved recipes/exercises or categories/types.

## Files

Now I'll present to you each of the files I've created or made changes to:

### models.py

In this file I've created all of my models, starting with CustomUser, in which I've added all of the necessary fields overriding AbstractUser, then Recipe model and LikedRecipe and Cookbook models that have CustomUser and Recipe as the foreign keys and of course similar with Exercise, LikedExercise and Training models.

### views.py

In this file it's the most going on I would say. I won't go so much to detail, but here all of the magic with the backend is happening. Removing, adding, changing, which there is a lot in this project, everything is happening here, and of course we can't forget displaying templates and register and login.

### fitness_app/urls.py

Here I really wanted my urls to be as clear and informative as possible, that's why in some of them i used both ids and slugs properties and included them in the url.

### scraper.py

This is a python file which uses BeautifulSoup and Selenium to scrape recipes data from website. (I've checked the terms and their policy and haven't found anything about scraping data). Scraping all of the data and saving it into variables so it can be easily grouped and accessed was really a fun part of this project.

### load_data.py

This file takes the data that *scraper.py* scraped and inserts it into the database.

### unslugify.py

This file contains the function I've needed to unslugify the titles to use them inside the template in "normal" form.

### styles.css 

In this file, there is css code that i wrpte for this app.

### categories.html

This template displays all of the recipes categories with their counts.

### category.html

This template displays all recipes within chosen category.

### exercises.html

This template displays all exercises and ability to add another and also like/unlike save/unsave them.

### exercise.html

This template displays chosen exercise with the description.

### index.html

This template displays the profile page, where is the double navigation for your recipes, exercises and personal data, counts liked/saved recipes/exercises and updates itself using javascript. This template is the biggest one and took a lot of time.

### layout.html

This is just a base template, the whole structure of the page and all of the links, logo, bootstrap and other libraries.

### login.html

This template displays a login page.

### recipe.html

This template displays chosen recipe with ingredients and description.

### recipes.html

This template displays all recipes and ability to add another and also like/unlike save/unsave them.

### register.html

This template displays a register page with dynamic check for correct fields.

### search.html

This template displays the results of searching.

### type.html

This template displays all exercises within chosen category.

### types.html

This template displays all of the exercises types with their counts.
