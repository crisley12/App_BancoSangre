from kivymd.uix.screen import MDScreen
from kivy.lang import Builder



class LocationScreen(MDScreen):
  def __init__(self, **kwargs) -> None:
        Builder.load_file('screen_Kv/location_screen.kv')
        super().__init__(**kwargs)