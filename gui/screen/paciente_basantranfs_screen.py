from kivymd.uix.screen import MDScreen
from kivy.lang import Builder


#class SucesfulScreen(MDScreen):
    #pass

class PacienteBasantranfsScreen(MDScreen):
    def __init__(self, **kwargs) -> None:
        Builder.load_file('screen_Kv/paciente_basantranfs_screen.kv')
        super(PacienteBasantranfsScreen, self).__init__(**kwargs)
    