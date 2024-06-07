from kivymd.uix.backdrop.backdrop import MDCard
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
import requests

from config import API_KEY, API_URL

class WeatherCard(MDCard):
    def __init__(self , description, icon, temp, rain, wind, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids.desc_text.text = description
        self.ids.temp_text.text = f"{temp}°C"
        self.ids.rain_text.text = f"Ймовірність опадів: {rain*100}%"
        self.ids.wind_text.text = f"Швидкість вітру: {wind} м/c"
        self.ids.weather_icon.source = f"https://openweathermap.org/img/wn/{icon}@2x.png"
           

class MainScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def weather_search(self):
        self.ids.weather_carousel.clear_widgets()
        city = self.ids.city_field.text.strip().lower() #отримує з текостового поля назву міста
        api_params = { 
            "q": city, 
            "appid": API_KEY
        }
        
        data = requests.get(API_URL, api_params) # робимо запит по АПІ до сервісу погоди
        response = data.json() # отримуємо дані про погодуу форматі JSON
        print(response) 
        description = response["weather"][0]["description"] #опис погоди
        icon =  response["weather"][0]["icon"] # інонка
        temp = response["main"]["temp"] #температура
        if 'rain' in response:
            rain = response["rain"]["1h"]
        else:
            rain = 0
        wind = response["wind"]["speed"]        
        new_card = WeatherCard(description, icon, temp, rain, wind)
        self.ids.weather_carousel.add_widget(new_card)   




class WeatherApp(MDApp):
    def build(self):
        Builder.load_file('style.kv')
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        self.screen = MainScreen("main_screen")
        return self.screen

WeatherApp().run()