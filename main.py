from dotenv import load_dotenv
import requests
import os

# Load environment variables from the .env file
load_dotenv()

API_KEY = os.getenv('API_KEY')


def get_weather_data(api, place):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={place}&appid={
    api}&units=metric'

    try:
        response = requests.get(url)
        data = response.json()

        if data['cod'] != 200:
            print(f"Error: {data['message']}. You tried {place}. There was no "
                  f"trace of this city. Check the spelling and that the city exists. ")
            return None

        return {
            'city': data['name'],
            'temp': data['main']['temp'],
            'description': data['weather'][0]['description']
        }

    except requests.exceptions.RequestException as e:
        print(f"There was an error when fetching weather data for {place}:"
              f" {e}")
        return None


def display_weather():
    cities = input("Enter a single city, or enter multiple cities, separated "
                 "by a comma (e.g Glasgow,Paris,Istanbul): ").split(",")

    for city in cities:
        city = city.strip()
        weather = get_weather_data(API_KEY, city)

        if weather:
            print(f"Weather in {weather['city']}:\n"
                  f"Temperature: {weather['temp']}°C\n"
                  f"Description: {weather['description']}\n")
        else:
            print("Unable to retrieve weather data.")


if __name__ == "__main__":
    display_weather()
