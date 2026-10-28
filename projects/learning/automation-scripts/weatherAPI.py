
import requests

def get_weather(city):
    api_key = "API_KEY"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    print(f"Temperature: {data['main']['temp']}")

get_weather("Seattle")

