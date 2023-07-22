from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp


class RootAdmin(MDScreen):

    def __init__(self, **kwargs) -> None:
        Builder.load_file('views_kv/root_admin.kv')
        super().__init__(**kwargs)
        self.create_dropdown3()
        self.create_dropdown4()

#################################################
#            LISTA DESPLEGABLE
#################################################

    def create_dropdown3(self):

        items_3 = ['F', 'M']

        sexo_items = [
            {
                "viewclass": "OneLineListItem",
                "height": dp(30),
                "text": f"{i}",
                "on_release": lambda x=f"{i}": self.set_item3(x),
            } for i in items_3]
        self.sexo_medico = MDDropdownMenu(
            caller=self.ids.t_sexo_medico,
            items=sexo_items,
            position="bottom",
            width_mult=1,
            background_color=[1, 1, 1, 1],
            elevation=2
        )

    def set_item3(self, item):
        self.ids.t_sexo_medico.text = item
        self.sexo_medico.dismiss()

# segunda lista
    def create_dropdown4(self):

        items_4 = ['AB+', 'AB-', 'O+', 'O-', 'B+', 'B-', 'A+', 'A-']

        sangre_items = [
            {
                "viewclass": "OneLineListItem",
                "height": dp(30),
                "text": f"{i}",
                "on_release": lambda x=f"{i}": self.set_item4(x),
            } for i in items_4]
        self.sangre_medico = MDDropdownMenu(
            caller=self.ids.t_sangre_medico,
            items=sangre_items,
            position="bottom",
            width_mult=1.5,
            background_color=[1, 1, 1, 1],
            elevation=2
        )

    def set_item4(self, item):
        self.ids.t_sangre_medico.text = item
        self.sangre_medico.dismiss()


#################################################
#            INPUT CEDULA
#################################################

    Max_c = 8

    def check_length_cedula_medico(self):
        cedula_medico = self.ids.cedula_medico
        text = cedula_medico.text
        if len(text) > self.Max_c:
            cedula_medico.foreground_color = 1, 0, 0, 1  # Cambiar a color rojo
        else:
            cedula_medico.foreground_color = 0, 0, 0, 1  # Restaurar el color original


#################################################
#            INPUT N_TELEFONO
#################################################

    Max_t = 11

    def check_length_telefono(self):
        telefono_medico = self.ids.n_telefono_medico
        text = telefono_medico.text
        if len(text) > self.Max_t:
            telefono_medico.foreground_color = 1, 0, 0, 1
        else:
            telefono_medico.foreground_color = 0, 0, 0, 1


class ContentNavigationDrawerr(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()
