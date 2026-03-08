import requests

API_KEY = "6c2bcaa18bcbef5e202402501806797f"

def get_weather(city):

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]

    rainfall = data.get("rain", {}).get("1h", 0)

    return temp, humidity, rainfall