import requests



def get_weather():
    api_url = "https://api.open-meteo.com/v1/forecast?latitude=30.0626&longitude=31.2497&current=temperature_2m,is_day,cloud_cover,wind_speed_10m&timezone=Africa%2FCairo"

    response = requests.get(api_url)

    return response.json()