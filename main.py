from kivymd.uix.backdrop.backdrop import MDCard
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
import requests

from config import API_KEY, API_URL


class WeatherCard(MDCard):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
    

class MainScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def weather_search(self):
        city = self.ids.city_field.text.strip().lower() #отримує з текостового поля назву міста
        api_params = { 
            "q": city, 
            "appid": API_KEY
        }
        
        data = requests.get(API_URL, api_params) # робимо запит по АПІ до сервісу погоди
        response = data.json() # отримуємо дані про погодуу форматі JSON
        print(response) 
        description = response["weather"][0]["description"]
        
        self.ids.weather_card.ids.label.text = description      


class WeatherApp(MDApp):
    def build(self):
        Builder.load_file('style.kv')
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        self.screen = MainScreen("main_screen")
        return self.screen

WeatherApp().run()