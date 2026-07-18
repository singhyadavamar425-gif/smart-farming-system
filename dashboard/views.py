import requests
from django.shortcuts import render

# ==========================
# Weather API Key
# ==========================

API_KEY = "d97edf216eac45fcb2421514260607"

# ==========================
# Live Weather Function
# ==========================

def get_weather(city="Gorakhpur"):

    try:

        url = (
            f"http://api.weatherapi.com/v1/current.json"
            f"?key={API_KEY}&q={city}&aqi=yes"
        )

        response = requests.get(url, timeout=5)

        response.raise_for_status()

        data = response.json()

        return {

            "city": data["location"]["name"],

            "temperature": data["current"]["temp_c"],

            "humidity": data["current"]["humidity"],

            "wind": data["current"]["wind_kph"],

            "condition": data["current"]["condition"]["text"],

            "icon": "https:" + data["current"]["condition"]["icon"]

        }

    except Exception:

        return {

            "city": city,

            "temperature": "--",

            "humidity": "--",

            "wind": "--",

            "condition": "Unavailable",

            "icon": ""

        }

# ==========================
# Dashboard
# ==========================

def dashboard(request):

    weather = get_weather()

    return render(
        request,
        "dashboard/index.html",
        {
            "weather": weather
        }
    )

# ==========================
# Profile
# ==========================

def profile(request):

    return render(
        request,
        "dashboard/profile.html"
    )