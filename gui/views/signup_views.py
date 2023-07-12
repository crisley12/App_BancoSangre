from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineIconListItem
from kivy.metrics import dp
# from kivymd.uix.pickers import MDDatePicker
# from kivymd.theming import ThemeManager


class Signup(MDScreen):

    def __init__(self, **kwargs) -> None:
        Builder.load_file("views_kv/signup.kv")
        super(Signup, self).__init__(**kwargs)
        self.f_nacimiento = self.ids.f_nacimiento
        self.create_dropdown1()
        self.create_dropdown2()

#################################################
#            LISTA DESPLEGABLE
#################################################

    def create_dropdown1(self):

        items_1 = ['F', 'M']

        sexo_items = [
            {
                "viewclass": "OneLineListItem",
                "height": dp(30),
                "text": f"{i}",
                "on_release": lambda x=f"{i}": self.set_item(x),
            } for i in items_1]
        self.sexo = MDDropdownMenu(
            caller=self.ids.t_sexo,
            items=sexo_items,
            position="bottom",
            width_mult=1,
            background_color=[1, 1, 1, 1],
            elevation=2
        )

    def set_item(self, text__item):
        self.ids.t_sexo.text = text__item
        self.sexo.dismiss()

# segunda lista
    def create_dropdown2(self):

        items_2 = ['AB+', 'AB-', 'O+', 'O-', 'B+', 'B-', 'A+', 'A-']

        sangre_items = [
            {
                "viewclass": "OneLineListItem",
                "height": dp(30),
                "text": f"{i}",
                "on_release": lambda x=f"{i}": self.set_item(x),
            } for i in items_2]
        self.sangre = MDDropdownMenu(
            caller=self.ids.t_sexo,
            items=sangre_items,
            position="bottom",
            width_mult=1.5,
            background_color=[1, 1, 1, 1],
            elevation=2
        )

    def set_item(self, text__item):
        self.ids.t_sangre.text = text__item
        self.sangre.dismiss()


#################################################
#            INPUT CEDULA
#################################################

    Max_c = 10

    def check_length_cedula(self):
        cedula = self.ids.cedula
        text = cedula.text
        if len(text) > self.Max_c:
            cedula.foreground_color = 1, 0, 0, 1  # Cambiar a color rojo
        else:
            cedula.foreground_color = 0, 0, 0, 1  # Restaurar el color original


#################################################
#            INPUT N_TELEFONO
#################################################

    Max_t = 11

    def check_length_telefono(self):
        telefono = self.ids.n_telefono
        text = telefono.text
        if len(text) > self.Max_t:
            telefono.foreground_color = 1, 0, 0, 1
        else:
            telefono.foreground_color = 0, 0, 0, 1


'''
    def create_dropdown(self):
        self.dropdown_1 = DropDown()
        self.dropdown_2 = DropDown()
      

        items_1 = ['AB+', 'AB-', 'O+', 'O-', 'B+', 'B-', 'A+', 'A-']
        for item_text in items_1:
            item = OneLineListItem(text=item_text)
            item.bind(on_release=self.menu_callback_1)
            self.dropdown_1.add_widget(item) 

        
        items_2 = ['F', 'M']
        for item_text in items_2:
            item = OneLineListItem(text=item_text)
            item.bind(on_release=self.menu_callback_2)
            self.dropdown_2.add_widget(item)

    def menu_callback_1(self, instance) -> None:
        selected_text = instance.text
        print(selected_text)
        self.t_sangre.text = selected_text
        self.dropdown_1.dismiss()

    def menu_callback_2(self, instance) -> None:
        selected_text = instance.text
        print(selected_text)
        self.t_sexo.text = selected_text
        self.dropdown_2.dismiss()

'''
