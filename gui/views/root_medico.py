from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
#from kivymd.uix.scrollview import MDScrollView


class RootMedico(MDScreen):
    def __init__(self, **kwargs) -> None:
        Builder.load_file('views_kv/root_medico.kv')
        super().__init__(**kwargs)


class ContentNavigationDrawerr(MDScreen):
    screen = ObjectProperty()
    nav = ObjectProperty()
