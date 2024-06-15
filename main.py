from kivymd.uix.backdrop.backdrop import MDCard
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
import requests

from config import API_KEY, API_URL, FORECAST_URL

class WeatherCard(MDCard):
    def __init__(self , date_time, description, icon, temp, rain, wind, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids.date_text.text = date_time
        self.ids.desc_text.text = description
        self.ids.temp_text.text = f"{temp}°C"
        self.ids.rain_text.text = f"Ймовірність опадів: {rain*100}%"
        self.ids.wind_text.text = f"Швидкість вітру: {wind} м/c"
        self.ids.weather_icon.source = f"https://openweathermap.org/img/wn/{icon}@2x.png"
           

class MainScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_weather_data(self, url, city):
        """Функція робить запиит до сайту погоди і повертає JSON з даними"""
        api_params = { 
            "q": city, 
            "appid": API_KEY
        }
        
        data = requests.get(url, api_params) # робимо запит по АПІ до сервісу погоди
        if data.status_code == 200:
            response = data.json() # отримуємо дані про погодуу форматі JSON
            return response
        else:
            return None

    def add_weather_card(self, response):
        description = response["weather"][0]["description"] #опис погоди
        icon =  response["weather"][0]["icon"] # інонка
        temp = response["main"]["temp"] #температура
        if 'rain' in response:
            if "1h" in response["rain"]:
                rain = response["rain"]["1h"]
            else:
                rain = response["rain"]["3h"]
        else:
            rain = 0
        wind = response["wind"]["speed"]
        if "dt_txt" in response:
            date_time = response['dt_txt'][5:-3]  
        else:
            date_time = "Зараз"   
        new_card = WeatherCard(date_time, description, icon, temp, rain, wind)
        self.ids.weather_carousel.add_widget(new_card)  

    def weather_search(self):
        self.ids.weather_carousel.clear_widgets()
        city = self.ids.city_field.text.strip().lower() #отримує з текостового поля назву міста
        current_weather = self.get_weather_data(API_URL,city)
        forecast = self.get_weather_data(FORECAST_URL, city)
        
        if current_weather:
            self.add_weather_card(current_weather)

        if forecast:
            for period in forecast['list']:
                self.add_weather_card(period)


class WeatherApp(MDApp):
    def build(self):
        Builder.load_file('style.kv')
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        self.screen = MainScreen("main_screen")
        return self.screen

WeatherApp().run()