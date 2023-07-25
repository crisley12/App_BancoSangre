from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
import os
import webbrowser
from kivy.utils import platform


class LocationScreen(MDScreen):
    pass


class GroupSangre(MDScreen):
    pass


class UserScreen(MDScreen):
    pass


class RootScreen(MDScreen):
    def __init__(self, **kwargs) -> None:
        Builder.load_file('views_kv/root_screen.kv')
        super().__init__(**kwargs)

    def open_google_maps(self, instance):

        url = "https://maps.app.goo.gl/6E72o1oQS66Fv67H8"

        if platform == "android":
            # Abre la aplicación de Google Maps en Android
            os.system(f"am start -a android.intent.action.VIEW -d {url}")
        elif platform == "ios":
            # Abre la aplicación de Google Maps en iOS
            os.system(f"open {url}")
        else:
            # Abre la URL en el navegador web en otras plataformas
            webbrowser.open(url)

    def open_whatsapp(self, instance):

        url = "https://wa.me/584165029813"
        if platform == "android":
            os.system(f"am start -a android.intent.action.VIEW -d {url}")
        elif platform == "ios":
            os.system(f"open {url}")
        else:
            webbrowser.open(url)

    def open_facebook(self, instance):

        url = "https://www.facebook.com/basantranfsb?mibextid=ZbWKwL"
        if platform == "android":
            os.system(f"am start -a android.intent.action.VIEW -d {url}")
        elif platform == "ios":
            os.system(f"open {url}")
        else:
            webbrowser.open(url)

    def open_instagram(self, instance):

        url = "https://instagram.com/basantranfs?igshid=MzRlODBiNWFlZA=="
        if platform == "android":
            os.system(f"am start -a android.intent.action.VIEW -d {url}")
        elif platform == "ios":
            os.system(f"open {url}")
        else:
            webbrowser.open(url)

    '''
    def __init__(self, directory, **kwargs):
        super(RootScreen, self).__init__(**kwargs)
        self.directory = directory
        self.load_all_kv_files()

    def load_all_kv_files(self):
        kv_files = [
            'screen_Kv/menu_screen.kv', 
            'screen_Kv/user_screen.kv'
        ]

        for kv_file in kv_files:
            Builder.load_file(os.path.join(self.directory, kv_file))
    '''
