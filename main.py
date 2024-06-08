from kivymd.uix.pickers.datepicker.datepicker import date
from kivymd.uix.backdrop.backdrop import MDCard
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.screen import MDScreen
from kivy.storage.jsonstore import JsonStore
import requests

from config import API_KEY, API_URL, FORECAST_URL

class WeatherCard(MDCard):
    def __init__(self ,date_text, description, icon, temp, rain, wind, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids.date_text.text = date_text
        self.ids.desc_text.text = description.capitalize()
        self.ids.temp_text.text = f"{temp}°C"
        self.ids.rain_text.text = f"Ймовірність опадів: {rain*100}%"
        self.ids.wind_text.text = f"Швидкість вітру: {wind} м/c"
        self.ids.weather_icon.source = f"https://openweathermap.org/img/wn/{icon}@2x.png"
           

class MainScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.store = JsonStore('last_city.json')
        self.load_last_city()

    def load_last_city(self):
        if self.store.exists('last_city'):
            last_city = self.store.get('last_city')['name']
            self.ids.city_field.text = last_city.capitalize()
            self.weather_search()

    def weather_search(self):
        self.ids.weather_carousel.clear_widgets()
        city = self.ids.city_field.text.strip().lower()
        # Збереження останнього введеного міста
        self.store.put('last_city', name=city)
        current_weather = self.get_weather_data(API_URL, city)
        forecast = self.get_weather_data(FORECAST_URL, city)

        if current_weather:
            self.add_weather_card("Зараз", current_weather)

        if forecast:
            for period in forecast['list'][1::2]:
                date = period['dt_txt'][5:-3]
                self.add_weather_card(date, period)

    def get_weather_data(self, url, city):
        api_params = {"q": city, "appid": API_KEY}
        response = requests.get(url, api_params)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def add_weather_card(self, date, data):
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        rain = data.get('rain', {}).get('1h', 0) if date == "Зараз" else data.get('rain', {}).get('3h', 0)
        wind = data['wind']['speed']
        new_card = WeatherCard(date, description, icon, temp, rain, wind)
        self.ids.weather_carousel.add_widget(new_card)

    def show_about_dialog(self):
        dialog = MDDialog(
            title="Про розробника",
            text="Цей додаток був розроблений в школі Logika. Для контакту: ваш_email@example.com",
            buttons=[
                MDRaisedButton(
                    text="Закрити",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()


class WeatherApp(MDApp):
    def build(self):

        Builder.load_file('style.kv')
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        self.screen = MainScreen("main_screen")
        return self.screen

WeatherApp().run()