import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


def scraper(amount):
    # set headless mode
    options = Options()
    options.headless = True

    # create webdriver instance
    driver = webdriver.Chrome(options=options)
    url = "https://www.gordonramsay.com/gr/recipes/category/fit-food"
    driver.get(url)
    time.sleep(2)  # Wait for page to load

    cookies = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[4]/div[1]/div[2]/button[4]")
    cookies.click()

    # Use Beautiful Soup to extract recipe information
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    button = driver.find_element(by=By.CLASS_NAME, value="button")
    button.click()

    data = []

    try:
        for _ in range(amount):
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            site = soup.find('section', class_='recipe-block-preview')
            title = site.find('h2').text.strip()
            image_url = "https://www.gordonramsay.com/" + site.find('img').get('src')
            
            recipe = soup.find('div', class_="recipe-container")
            uls = recipe.find_all('ul', class_="recipe-division")
            ol = recipe.find('ol', class_="recipe-division")

            categories = []
            categories_ul = soup.find('ul', class_='categories')
            for lis in categories_ul.find_all('li'):
                for link in lis.find_all('a', class_='active'):
                    item = link.find('span')
                    if link:
                        categories.append(item.text.strip())
                
            ingredients = []
            for ul in uls:
                for li in ul.find_all('li'):
                    for item in li:
                        ingredients.append(item.get_text().strip())
            
            if len(ingredients) == 0:
                p = soup.find_all('p', class_='recipe-division')
                for ingredient in p:
                    ingredients.append(ingredient.text.strip())
            
            recipe = []
            for li in ol.find_all('li'):
                for item in li:
                    recipe.append(item.get_text().strip())
            
            dict = {"title": "", "image": "", "categories": "", "ingredients": "", "recipe": ""}
            
            dict["title"] = title
            dict["image"] = image_url
            dict["categories"] = categories
            dict["ingredients"] = ingredients
            dict["recipe"] = recipe

            data.append(dict)
            
            next = driver.find_element(by=By.CLASS_NAME, value="next")
            if next:
                next.find_element(By.TAG_NAME, 'a').click()
    except Exception as e:
        print(f"Error occured while scraping: {e}")

    # Close the Selenium webdriver
    driver.quit()

    return data