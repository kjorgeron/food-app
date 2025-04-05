import requests
import time
from requests.exceptions import RequestException

# Base URL for TheMealDB API
BASE_URL = "https://themealdb.com/api/json/v1/1/"

def get_all_categories():
    """
    Retrieve all recipe categories with error handling.
    """
    try:
        response = requests.get(BASE_URL + "categories.php", timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        return [category["strCategory"] for category in data["categories"]]
    except RequestException as e:
        print(f"Error fetching categories: {e}")
        return []

def get_recipes_by_category(category):
    """
    Retrieve all recipes for a specific category with retry logic.
    """
    attempts = 3
    for attempt in range(attempts):
        try:
            print(f"Fetching recipes for category: {category} (Attempt {attempt + 1})")
            response = requests.get(BASE_URL + f"filter.php?c={category}", timeout=10)
            response.raise_for_status()
            data = response.json()
            return data["meals"] if data["meals"] else []
        except RequestException as e:
            print(f"Error fetching recipes for category {category}: {e}")
            if attempt < attempts - 1:  # Retry if attempts remain
                time.sleep(2)  # Delay before retrying
            else:
                print(f"Failed to fetch recipes for category: {category} after {attempts} attempts.")
                return []

def collect_all_recipes():
    """
    Collect all recipes from TheMealDB with error handling and delay.
    """
    all_recipes = {}
    categories = get_all_categories()
    print(f"Found {len(categories)} categories.")

    for category in categories:
        recipes = get_recipes_by_category(category)
        if recipes:
            all_recipes[category] = recipes
        time.sleep(1)  # Add delay between category requests to avoid server overload
    
    return all_recipes

# Example usage
all_recipes = collect_all_recipes()
print(f"\nCollected recipes from {len(all_recipes)} categories.")

# Displaying the first recipe from each category (if available)
for category, recipes in all_recipes.items():
    if recipes:
        print(f"\nCategory: {category}")
        print(f"First Recipe: {recipes[0]['strMeal']}")
        print(f"Recipe ID: {recipes[0]['idMeal']}")