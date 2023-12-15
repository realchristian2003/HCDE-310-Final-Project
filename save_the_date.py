#save_the_date.py
#Christian Real, Yuri Yang


import requests #use pip install request HTTP requests
import pycountry #before adding this to our code, we were having trouble getting the recipes because
#for Calendarific, it would be in an ISO format, then we looked up how to convert the ISO format
#to using it to guse for Country name

#for recipe key
EDAMAM_API_KEY = '0cc48e45c5362bfae2c8274d59d899f4'
EDAMAM_APP_ID = '976dc691'

#holidays
CALENDARIFIC_API_KEY = 'FQ8YjleALRgwLOZoX3S7yJi53cH9cKZV'


def get_recipes(preferences, holiday=None):
    """
    Get curated recipes based on your preference.
    """
    endpoint = 'https://api.edamam.com/api/recipes/v2'
    params = {
        'q': preferences.get('cuisine', 'any'),
        'diet': preferences.get('diet', 'balanced'),
        'health': preferences.get('health', ''),
        'app_id': EDAMAM_APP_ID,
        'app_key': EDAMAM_API_KEY,
    }

    # Include holiday parameter if specified
    if holiday:
        params['q'] += f" {holiday} recipes"

    response = requests.get(endpoint, params=params)

    print(f"Edamam API Request URL: {response.url}")

    if response.status_code == 200:
        data = response.json()
        recipes = data.get('hits', [])
        if recipes:
            return [{'name': recipe['recipe']['label'], 'details': recipe['recipe']} for recipe in recipes]
        else:
            print("No recipes found in the response.")
    else:
        print(f"Error fetching recipes: {response.status_code}")
    return []


def get_country_iso_code(country_name):
    """
    Get ISO-3166 country code from country name.
    """
    try:
        country_info = pycountry.countries.get(name=country_name)
        return country_info.alpha_2
    except AttributeError:
        print("Invalid country name.")
        return None


def get_holidays(country_iso_code, year):
    """
    Get holidays based on the country and year using Calendarific API.
    """
    endpoint = 'https://calendarific.com/api/v2/holidays'
    params = {
        'api_key': CALENDARIFIC_API_KEY,
        'country': country_iso_code,
        'year': year,
    }

    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        data = response.json()

        if isinstance(data, list):
            # Handle the case where the response is a list
            return [item['name'] for item in data]
        elif isinstance(data, dict):
            # Handle the case where the response is a dictionary
            holidays = data.get('response', {}).get('holidays', [])
            return [holiday['name'] for holiday in holidays]
    print(f"Error fetching holidays: {response.status_code}")
    return []


def main():
    print("Welcome to Save the Date!- Where thinking what to cook on a special day won't be a problem anymore!")

    # Collect user preferences
    cuisine = input("Enter your preferred cuisine (e.g., Italian, Mexican, Asian): ")
    diet = input("Any specific dietary restrictions (e.g., balanced, low-carb): ")
    health = input("Any specific health labels (e.g., vegan, vegetarian): ")
    country_name = input("Enter your country for holiday information: ")
    year = input("Enter the year for holiday information: ")

    # Convert country name to ISO format
    country_iso_code = get_country_iso_code(country_name)

    if country_iso_code:
        preferences = {'cuisine': cuisine, 'diet': diet, 'health': health}

        # Get holidays based on the country and year
        holidays = get_holidays(country_iso_code, year)

        if holidays:
            print("\nSelect a holiday for recipe suggestions:")
            for idx, holiday in enumerate(holidays, start=1):
                print(f"{idx}. {holiday}")

            selected_index = int(input("Enter the number corresponding to the desired holiday: "))

            if 1 <= selected_index <= len(holidays):
                selected_holiday = holidays[selected_index - 1]
                print(f"\nRecipes for {selected_holiday}:")

                # Get curated recipes based on user preferences and selected holiday
                recipes = get_recipes(preferences, holiday=selected_holiday)

                if recipes:
                    for idx, recipe in enumerate(recipes, start=1):
                        print(f"{idx}. Recipe: {recipe['name']}")
                        print("   Details:", recipe['details'])
                else:
                    print("No recipes found. Please adjust your preferences.")
            else:
                print("Invalid selection. Exiting.")
        else:
            print("No holidays found for the specified country and year.")


if __name__ == "__main__":
    main()




