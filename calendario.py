'''
    def on_save(self, instance, value, date_range):
        
        
        Eventos a los que se llama cuando se hace clic en el botón del cuadro de diálogo "Aceptar".

        :type instance: <kivymd.uix.picker.MDDatePicker object>;
        :param value: Fecha;
        :type value: <class 'datetime.date'>;
        :param date_range: lista de 'datetime.date' objetos del rango seleccionado;
        :type date_range: <class 'list'>;
        
        date_text = value.strftime('%Y-%m-%d')  # Convierte la fecha en formato de texto
        self.ids.f_nacimiento.text = date_text  # Actualiza el texto del campo de entrada
        print(instance, value, date_range)


    def on_cancel(self, instance, value):
        Eventos a los que se llama cuando se hace clic en el botón del cuadro de diálogo "CANCELAR".

      # def on_device_orientation(self, instance_theme_manager: ThemeManager, orientation_value: str)


# crea y muestra un cuadro de diálogo de selección de fecha con varias configuraciones personalizadas.
    def show_date_picker(self):
        date_dialog = MDDatePicker(
          title_input="fecha de Nacimiento",
          title="fecha de Nacimiento",
          primary_color=(240/255, 0/255, 0/255),
          accent_color=(255/255, 255/255, 255/255),
          selector_color=(240/255, 0/255, 0/255),
          text_toolbar_color=(255/255, 255/255, 255/255),
          text_weekday_color=(240/255, 0/255, 0/255),
          text_current_color=(255/255, 255/255, 255/255),
          text_button_color=(240/255, 0/255, 0/255),
          font_name="asset/Fuentes/Poppins-SemiBold.ttf",
          helper_text= "Error",
          min_year=1923, 
          max_year=2006, 
          year=2002, 
          month=9, 
          day=18)
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

'''
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty

from kivymd.uix.list import OneLineIconListItem
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu

KV = '''
<IconListItem>

    IconLeftWidget:
        icon: root.icon


MDScreen

    MDTextField:
        id: field
        pos_hint: {'center_x': .5, 'center_y': .6}
        size_hint_x: None
        width: "200dp"
        hint_text: "Password"
        on_focus: if self.focus: app.menu.open()



'''

'''
 https://kivymd.readthedocs.io/en/1.1.1/components/menu/index.html
'''

class IconListItem(OneLineIconListItem):
    icon = StringProperty()


class Test(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)
        
        items_1 = ['AB+', 'AB-', 'O+', 'O-', 'B+', 'B-', 'A+', 'A-']

        menu_items = [
            {
                "viewclass": "IconListItem",
                "height": dp(56),
                "text": f"{i}",
                "on_release": lambda x=f"{i}": self.set_item(x),
            } for i in items_1]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.field,
            items=menu_items,
            position="bottom",
            width_mult=3,
        )

        

    def set_item(self, text__item):
        self.screen.ids.field.text = text__item
        self.menu.dismiss()

    def build(self):
        return self.screen


Test().run()

'''
MDFloatLayout:
            id: dropdown_2
            MDRaisedButton:
                id: t_sexo
                icon: 'gender-male-female'
                text: "Sexo"
                md_bg_color: (238/255, 238/255, 1)
                text_color: 240/255, 0/255, 0/255
                padding: [30, 0]
                size_hint: .25, .05
                pos_hint: {"center_x": .50, "center_y": .56}
                on_release: root.dropdown_2.open(self)
            MDBoxLayout:
                id: items_2
                orientation: 'vertical'
                size_hint_y: None
                height: "40dp"
'''
