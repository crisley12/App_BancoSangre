from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window


Window.size = (350, 600)

class Main(MDApp):
    def build(self) -> None:
        global screen_manager
        screen_manager = ScreenManager()
        #self.manager = ScreenManager(transition = NoTransition())
        screen_manager.add_widget(Builder.load_file("main.kv"))
        screen_manager.add_widget(Builder.load_file("login.kv"))
        screen_manager.add_widget(Builder.load_file("signup.kv"))
        return screen_manager

    def on_start(self) -> None:
        Clock.schedule_once(self.login, 3)

    def login(self, *args) -> None:
        screen_manager.current = "login"

if __name__== '__main__':
    Main().run()