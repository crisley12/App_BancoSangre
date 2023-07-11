from kivymd.uix.screen import MDScreen
from kivy.lang import Builder



class NeedDonateScreen(MDScreen):
  def __init__(self, **kwargs) -> None:
        Builder.load_file('screen_Kv/need_donate_screen.kv')
        super().__init__(**kwargs)