from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
import requests
import logging


class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()
    #root_admin_instance = None

class RootAdmin(MDScreen):
    data_table = ObjectProperty(None)
    # sexo_medico = ObjectProperty(None)
    pacientes_data = []
    logging.basicConfig(filename='app_debug.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
    paciente_id = None
    

    def __init__(self, **kwargs) -> None:
        Builder.load_file('views_kv/root_admin.kv')
        super().__init__(**kwargs)
        #ContentNavigationDrawer.root_admin_instance = self 
        self.create_dropdown3()
        self.create_dropdown4()
        self.obtener_pacientes()

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



#################################################
#            MOSTRAR PACIENTES
#################################################
    def obtener_pacientes(self):
        response = requests.get('http://localhost:5000/obtener_pacientes')
        datos_pacientes = response.json()
        print("Datos de pacientes recibidos desde el servidor:", datos_pacientes)
        # Asignar los datos de pacientes recibidos al atributo pacientes_data del cliente
        self.pacientes_data = datos_pacientes

        if response.status_code == 200:
            paciente_data = []
            for i, item in enumerate(self.pacientes_data, start=0):
                if isinstance(item, dict):
                    row = (
                        # Obtener el valor correspondiente a cada columna en la fila
                        f"{i}",  # Número como cadena
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
                elevation=1,
                background_color_header="#F41F05",
                check=True,
                column_data=[
                    ("No.", dp(30)),
                    ("Cédula", dp(30)),
                    ("Nombre", dp(30)),
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


#################################################
#            ELIMINAR PACIENTES
#################################################
    def eliminar_pacientes(self):
        print("Botón de eliminar pacientes presionado.")
        print("Datos de pacientes:")
        print(self.pacientes_data)
        
        filas_seleccionadas = self.data_table.get_row_checks()  # Obtener filas seleccionadas en la tabla
        if filas_seleccionadas:
            # Obtener los IDs de los pacientes seleccionados
            pacientes_a_eliminar = []
            for index_list in filas_seleccionadas:
                index = int(index_list[0])  # Convertir el índice a enterox``
                paciente_id = self.pacientes_data[index]['id']
                print(f"Enviando al servidor para eliminar paciente con ID: {paciente_id}")
                pacientes_a_eliminar.append(paciente_id)

            for paciente_id in pacientes_a_eliminar:
                # Hacer la solicitud al servidor de Flask para eliminar el paciente
                url_eliminar = f"http://localhost:5000/eliminar_paciente/{paciente_id}"
                response = requests.post(url_eliminar)

                if response.status_code == 200:
                    # Si la eliminación fue exitosa en el servidor, eliminar el paciente del self.pacientes_data
                    self.pacientes_data = [row for row in self.pacientes_data if row['id'] not in pacientes_a_eliminar]
                    # Actualizar la tabla en la interfaz con la nueva lista de pacientes
                    self.obtener_pacientes()        
                else:
                    print(f"Error al eliminar el paciente con ID {paciente_id} en el servidor")
        else:
            print("Por favor, seleccione al menos un paciente para eliminar.")
            
  

    def on_row_press(self, instance_table, instance_row):
        print("Se presionó una fila:", instance_row)


    def on_check_press(self, instance_table, current_row):
        print("Se presionó el checkbox de la fila:", current_row)