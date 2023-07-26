from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
import requests


class DonacionesScreen(MDScreen):
    def __init__(self, **kwargs) -> None:
          Builder.load_file('screen_Kv/donaciones_screen.kv')
          super().__init__(**kwargs)
