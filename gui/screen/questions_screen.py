from kivymd.uix.screen import MDScreen
from kivy.lang import Builder



class QuestionsScreen(MDScreen):
  def __init__(self, **kwargs) -> None:
        Builder.load_file('screen_Kv/questions_screen.kv')
        super().__init__(**kwargs)