import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness.settings')
django.setup()

from fitness_app.models import Recipe
from scraper import scraper

def load_data(amount):
    # Call the scrape function to retrieve data
    data = scraper(amount)

    # Save the data to the database
    for item in data:
        recipe = Recipe(title=item['title'], ingredients=item['ingredients'], image=item['image'], recipe=item['recipe'], categories=item['categories'])
        recipe.save()

if __name__ == '__main__':
    load_data(100)