## Distinctiveness and Complexity

I believe my project satisfies the distinctiveness and complexity requirements because I have made efforts to create a versatile fitness app. The app allows users to create personal accounts with information such as birth date, height, weight, etc. Users can modify their data as they progress in their fitness journey. The app is divided into three main sections:

1. Profile: This section contains liked/saved recipes and exercises, as well as personal data.

2. Recipes: This section includes a collection of recipes.

3. Exercises: This section contains various exercises.

Some key features that demonstrate the fulfillment of requirements are:

- Ability to like/unlike and save/unsave recipes and exercises.
- Ability to add custom recipes/exercises to the database.
- Enhanced user experience using JavaScript for interactivity.
- The profile section has a "double navigation" feature that remembers the state after page reload.
- A search bar with the option to search for exercises or recipes.
- A clean and visually pleasing design with small animations and thoughtful details, such as dynamic counts of liked/saved recipes/exercises and categories/types.

## Files

Now, let's go through each of the files created or modified for the project:

- `models.py`: Contains all the necessary models, including `CustomUser` which overrides `AbstractUser`, as well as `Recipe`, `LikedRecipe`, `Cookbook`, `Exercise`, `LikedExercise`, and `Training` models.

- `views.py`: Handles backend logic, including adding, removing, and modifying data. Also responsible for rendering templates, registration, and login functionality.

- `fitness_app/urls.py`: Defines clear and informative URLs, utilizing both IDs and slugs for better readability.

- `scraper.py`: A Python file that utilizes BeautifulSoup and Selenium to scrape recipe data from a website. Note: Make sure to review the website's terms and policies regarding data scraping.

- `load_data.py`: Loads the data scraped by `scraper.py` into the database.

- `unslugify.py`: Contains a function to convert slugs into readable titles for use in templates.

- `styles.css`: Contains the CSS code for the app.

- `categories.html`: Template displaying all recipe categories with their respective counts.

- `category.html`: Template displaying all recipes within a chosen category.

- `exercises.html`: Template displaying all exercises, allowing addition, liking/unliking, and saving/unsaving.

- `exercise.html`: Template displaying a selected exercise with its description.

- `index.html`: Template representing the profile page. It includes a double navigation feature for accessing recipes, exercises, and personal data. It also dynamically updates the counts of liked/saved recipes/exercises using JavaScript.

- `layout.html`: Base template containing the overall page structure, including links, logo, and libraries such as Bootstrap.

- `login.html`: Template for the login page.

- `recipe.html`: Template displaying a selected recipe with ingredients and description.

- `recipes.html`: Template displaying all recipes, allowing addition, liking/unliking, and saving/unsaving.

- `register.html`: Template for the registration page, featuring dynamic field validation.

- `search.html`: Template displaying search results.

- `type.html`: Template displaying all exercises within a chosen category.

- `types.html`: Template displaying all exercise types with their respective counts.

## How to Run

To run the project, follow these steps:

1. Clone the repository to your local machine.

2. (Optional) Set up a virtual environment.

3. Activate the virtual environment.

4. Set up the database by running migrations:
   ```
   python manage.py migrate
   ```

5. Start the development server:
   ```
   python
