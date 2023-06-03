from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from views.login import Login
from views.signup import Signup

Window.size = (350, 600)


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.db = Database(database_name='banco_de_sangre')


# Constructor de la interfaz

    def build(self) -> None:
        global screen_manager
        screen_manager = ScreenManager()
        # self.manager = ScreenManager(transition = NoTransition())
        screen_manager.add_widget(Builder.load_file("kv/main.kv"))
        screen_manager.add_widget(Login(name='login'))
        screen_manager.add_widget(Signup(name='signup'))
        return screen_manager


# Transicion de pantalla de inicio a --> LoginScreen

    def on_start(self) -> None:
        Clock.schedule_once(self.login, 3)

    def login(self, *args) -> None:
        screen_manager.current = "login"


if __name__ == '__main__':
    MainApp().run()
