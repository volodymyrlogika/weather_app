from kivymd.uix.backdrop.backdrop import MDCard
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

class WeatherCard(MDCard):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)


class MainScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class WeatherApp(MDApp):
    def build(self):
        Builder.load_file('style.kv')
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        self.screen = MainScreen("main_screen")
        return self.screen

WeatherApp().run()