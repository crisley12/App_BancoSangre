from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from kivymd.uix.list import OneLineListItem
#from kivymd.uix.pickers import MDDatePicker
#from kivymd.theming import ThemeManager

class Signup(MDScreen):

    def __init__(self, **kwargs) -> None:
        Builder.load_file("kv/signup.kv")
        super(Signup, self).__init__(**kwargs)
        self.t_sangre = self.ids.t_sangre
        self.t_sexo = self.ids.t_sexo
        self.f_nacimiento = self.ids.f_nacimiento
        self.create_dropdown()
    

#################################################
#            SELECTOR DE FECHA
#################################################

#################################################
#            LISTA DESPLEGABLE
#################################################

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