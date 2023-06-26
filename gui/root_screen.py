from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
#from screen.menu_screen import MenuScreen
# from screen.user_screen import UserScreen


class RootScreen(MDScreen):
    def __init__(self, **kwargs) -> None:
        Builder.load_file('root_screen.kv')
        super().__init__(**kwargs)
        
        
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
