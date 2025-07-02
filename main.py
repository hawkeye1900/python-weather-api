from dotenv import load_dotenv
import requests
import os
from datetime import datetime
from sys import exit

# Load environment variables from the .env file
load_dotenv()

# Retrieve the api key
API_KEY = os.getenv('API_KEY')
if not API_KEY:
    print("Error: API key not found")
    exit(1)


def get_current_weather_data(api, place):
    params = {'q': place, 'appid': api, 'units': 'metric'}
    url = "http://api.openweathermap.org/data/2.5/weather"

    try:
        response = requests.get(url, params)
        data = response.json()

        # raise an exception if the HTTP response contains a client error
        # (4xx) or a server error (5xx) status code
        response.raise_for_status()

        return {
            'city': data['name'],
            'lat': data['coord']['lat'],
            'lon': data['coord']['lon'],
            'temp': data['main']['temp'],
            'description': data['weather'][0]['description']
        }

    except requests.exceptions.HTTPError as e:
        print(f"The following HTTP error occurred.\n{e}.")
        print("Try checking the spelling of your city before running the "
              "program again.")
        exit(-1)

    except requests.exceptions.RequestException as e:
        print(f"There was an error when fetching weather data for {place}:"
              f" {e}")
        exit(-1)


def get_5day_forecast(place, api):
    params = {'q': place, 'appid': api, 'units': 'metric'}
    url = "https://api.openweathermap.org/data/2.5/forecast"

    response = requests.get(url, params)
    data = response.json()

    return data


def display_weather():
    # protects against no input or an empty string input
    cities = ""
    while not cities or not cities[0].strip(",") or not cities[0].strip(" "):
        cities = input("Enter a single city, or enter multiple cities separated "
                       "by a comma (e.g Glasgow,Paris,Istanbul): \n")

    cities = cities.split(",")

    for city in cities:
        city = city.strip().title()
        weather = get_current_weather_data(API_KEY, city)

        if weather:
            print(f"Weather in {weather['city']} today:\n"
                  f"Temperature: {weather['temp']}°C\n"
                  f"Description: {weather['description']}\n")

        else:
            print("Unable to retrieve weather data.")
            exit()

        forecast = get_5day_forecast(city, API_KEY)

        if forecast:
            print(f"Displaying the 5-day forecast for {city}.")
            print("Forecast refers to 0700hrs on the date given\n")

            weather = forecast['list']
            for entry in weather:
                #  Getting the time stamp in utc
                stamp = (entry['dt'])

                # convert timestamp to date time
                entry_time = datetime.fromtimestamp(stamp)

                # Selecting entries for 0700hrs each day
                if entry_time.strftime("%H") == '07':
                    print(f"{entry_time.strftime("%a %d %b %Y")}:")
                    print(f"Weather: {entry['weather'][0]['description']}")
                    print(f"Max Temp: {round(entry['main']['temp_max'] 
                                             - 273.15, 2)}\u00b0C")
                    print(f"Max Temp: {round(entry['main']['temp_min']
                                             - 273.15, 2)}\u00b0C\n")


if __name__ == "__main__":
    display_weather()