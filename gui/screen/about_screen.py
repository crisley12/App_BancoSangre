from kivymd.uix.screen import MDScreen
from kivy.lang import Builder


class AboutScreen(MDScreen):
     def __init__(self, **kwargs) -> None:
        Builder.load_file('screen_Kv/about_screen.kv')
        super().__init__(**kwargs)