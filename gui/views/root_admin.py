from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
import requests



class RootAdmin(MDScreen):
    data_table = ObjectProperty(None)

    def __init__(self, **kwargs) -> None:
        Builder.load_file('views_kv/root_admin.kv')
        super().__init__(**kwargs)
        self.obtener_pacientes()

    def obtener_pacientes(self):
        urlpacientes = 'http://localhost:5000/obtener_pacientes'
        response = requests.get(urlpacientes)
        
        if response.status_code == 200:
            pacientes = response.json()
            paciente_data = []
            for item in pacientes:
                if isinstance(item, dict):
                    row = (
                        # Obtener el valor correspondiente a cada columna en la fila
                        item['cedula'],
                        item['nombre_completo'],
                        item['fecha_nacimiento'],
                        item['sexo'],
                        item['tipo_sangre'],
                        item['telefono'],
                    )
                    paciente_data.append(row)  # Agregar la fila a la lista de datos de filas

            # Crear el MDDataTable con los datos obtenidos
            self.data_table = MDDataTable(
                pos_hint={'center_y': 0.5, 'center_x': 0.5},
                size_hint=(0.9, 0.6),
                use_pagination=True,
                check=True,
                column_data=[
                    ("Cédula", dp(30)),
                    ("Nombre", dp(50)),
                    ("Fecha Nacimiento", dp(30)),
                    ("Sexo", dp(30)),
                    ("Tipo Sangre", dp(30)),
                    ("Telefono", dp(30)),
                ],
                row_data=paciente_data,  # Pasar la lista de datos de filas al MDDataTable
            )
            self.data_table.bind(on_row_press=self.on_row_press)
            self.data_table.bind(on_check_press=self.on_check_press)

            # Agregar el MDDataTable al layout
            self.ids.anchor_layout.add_widget(self.data_table)
        else:
            print("Error al obtener los pacientes")

    def on_row_press(self, instance_table, instance_row):
        print("Se presionó una fila:", instance_row)

    def on_check_press(self, instance_table, current_row):
        print("Se presionó el checkbox de la fila:", current_row)


    # def obtener_pacientes(self):
    #     urlpacientes = 'http://localhost:5000/obtener_pacientes'

    #     response = requests.get(urlpacientes)
    #     if response.status_code == 200:
    #         pacientes = response.json()
    #         paciente_data = []
    #         print(pacientes, "data")
    #         for item in pacientes:
    #             if isinstance(item, dict):
    #                 row = (
    #                     # Obtener el valor correspondiente a cada columna en la fila
    #                     item['cedula'],
    #                     item['nombre_completo'],
    #                     item['fecha_nacimiento'],
    #                     item['sexo'],
    #                     item['tipo_sangre'],
    #                     item['telefono'],
    #                 )
    #                 paciente_data.append(row)  # Agregar la fila a la lista de datos de filas

    #       # Crear el MDDataTable con los datos obtenidos
    #         #layout = AnchorLayout()
    #         self.data_tables = MDDataTable(
    #             pos_hint={'center_y': 0.5, 'center_x': 0.5},
    #             size_hint=(0.9, 0.6),
    #             use_pagination=True,
    #             check=True,
    #             column_data=[
    #                 ("Cédula", dp(30)),
    #                 ("Nombre", dp(50)),
    #                 ("Fecha Naciento", dp(30)),
    #                 ("Sexo", dp(30)),
    #                 ("Tipo Sangre", dp(30)),
    #                 ("Telefono", dp(30)),
    #             ],
    #             paciente_data=paciente_data,  # Pasar la lista de datos de filas al MDDataTable
    #         )
    #         self.data_tables.bind(on_row_press=self.on_row_press)
    #         self.data_tables.bind(on_check_press=self.on_check_press)
    #         self.data_tables.bind(on_check_press=self.on_check_press)

    #         self.data_table.bind(on_row_press=self.on_row_press)
    #         self.data_table.bind(on_check_press=self.on_check_press)

    #         # Agregar el MDDataTable al AnchorLayout
    #         anchor_layout = AnchorLayout(
    #             anchor_x='center', anchor_y='center'
    #         )
    #         anchor_layout.add_widget(self.data_table)
    #         self.add_widget(anchor_layout)

    #         self.checkcomprobar = 6
    #     else: print("error")

    # def on_enter(self):
    #         self.obtener_pacientes()

    # def on_row_press(self, instance_table, instance_row):
    #     '''Called when a table row is clicked.'''

    #     # print(instance_table, instance_row)

    # def on_check_press(self, instance_table, current_row):
    #     '''Called when the check box in the table row is checked.'''
    #     selected_rows = [row for row in self.data_tables.get_row_checks()]  # Obtener las filas seleccionadas
    #     if len(selected_rows) > 1:
    #         self.checkcomprobar = 2
    #         print("condicion mas de un check ", self.checkcomprobar)
    #     elif  len(selected_rows) <= 0:
    #         self.checkcomprobar = 3
    #         print("cNo ha marcado nada ", self.checkcomprobar)
    #     elif  len(selected_rows) == 1:
    #         print("Solo un checkbox seleccionado")
    #         self.checkcomprobar = 1
    #         self.globalselect = current_row
    #         print("condicion mas de un check ", self.checkcomprobar)
    #     else:
    #         self.checkcomprobar = 3
    # def on_enter(self):
    #         self.obtener_pacientes()


################################################
#          LISTA DESPLEGABLE
################################################


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

    def check_length_telefono_medico(self):
        telefono_medico = self.ids.n_telefono_medico
        text = telefono_medico.text
        if len(text) > self.Max_t:
            telefono_medico.foreground_color = 1, 0, 0, 1
        else:
            telefono_medico.foreground_color = 0, 0, 0, 1


class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()
