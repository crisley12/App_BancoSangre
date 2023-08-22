from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.datatables import MDDataTable
from datetime import datetime
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
import requests
import logging
import subprocess
import os


class CrearAdmin(MDScreen):
    pass
class CrearMedico(MDScreen):
    pass

class MostrarDonaciones(MDScreen):
    pass
class MostrarAdmin(MDScreen):
    pass
class MostrarMedico(MDScreen):
    pass

class MostrarPacientes(MDScreen):
    pass

class MostrarUsuarios(MDScreen):
    pass
class MostrarAuditoria(MDScreen):
    pass


class ContentNavigationDrawerAdmin(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()
    root_admin_instance = None


class RootAdmin(MDScreen):
    data_table = ObjectProperty(None)
    globalselect = []
    checkcomprobar = 5

    # sexo_medico = ObjectProperty(None)

    def __init__(self, **kwargs) -> None:
        Builder.load_file('views_kv/root_admin.kv')
        super().__init__(**kwargs)
        ContentNavigationDrawerAdmin.root_admin_instance = self
        self.create_dropdown3()
        self.create_dropdown4()
        self.obtener_usuarios()
        # self.obtener_pacientes()

###############################################
#         LISTA DESPLEGABLE
###############################################

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
#            MOSTRAR USUARIOS
#################################################

    def obtener_usuarios(self):
            urlusuarios = 'http://localhost:5000/obtener_usuarios'
            response = requests.get(urlusuarios)

            if response.status_code == 200:
                usuarios = response.json()
                usuario_data = []
                for i, item in enumerate(usuarios, start=1):
                    if isinstance(item, dict):
                        row = (
                            
                            f"{i}", 
                            item['email'],
                            item['paciente_id'],
                            item['role_id'],
                            item['id_usuario'],
                        )
                        usuario_data.append(row)

                self.data_table = MDDataTable(
                    pos_hint={'center_y': 0.4, 'center_x': 0.5},
                    size_hint=(0.9, 0.5),
                    use_pagination=True,
                    elevation=1,
                    background_color_header="#F41F05",
                    column_data=[
                        ("No.", dp(30)),
                        ("Email", dp(50)),
                        ("Cedula del Usuario", dp(50)),
                        ("Rol", dp(30)),
                        ("Id.", dp(50)),
                    ],
                    row_data=usuario_data, 
                )
                self.ids.usuarios.add_widget(self.data_table)
                self.checkcomprobar = 6
            else:
                print("Error al obtener los usuarios")






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

                        f"{i}",  
                        item['cedula'],
                        item['nombre_completo'],
                        item['apellido_completo'],
                        item['fecha_nacimiento'],
                        item['sexo'],
                        item['tipo_sangre'],
                        item['telefono'],
                    )
                    paciente_data.append(row)

            self.data_table = MDDataTable(
                pos_hint={'center_y': 0.4, 'center_x': 0.5},
                size_hint=(0.9, 0.5),
                use_pagination=True,
                elevation=1,
                background_color_header="#F41F05",
                check=True,
                column_data=[
                    ("No.", dp(30)),
                    ("Cédula", dp(30)),
                    ("Nombre", dp(30)),
                    ("Apellido", dp(30)),
                    ("Fecha Nacimiento", dp(30)),
                    ("Sexo", dp(30)),
                    ("Tipo Sangre", dp(30)),
                    ("Telefono", dp(30)),
                ],
                row_data=paciente_data,  
            )
            self.data_table.bind(on_row_press=self.on_row_press)
            self.data_table.bind(on_check_press=self.on_check_press)
            self.ids.anchor_layout.add_widget(self.data_table)
            self.checkcomprobar = 5
        else:
            print("Error al obtener los pacientes")


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
      
            
    def eliminar_medicos(self):
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
                    

    def eliminar_usuarios(self):
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


    def imprimir_pacientes(self):
        # Obtener la ruta completa al archivo pacientesPDF.py
        current_dir = os.path.dirname(os.path.abspath(__file__))
        reportes_dir = os.path.join(current_dir, "..", "reportes")
        pacientes_pdf_path = os.path.join(reportes_dir, "pacientesPDF.py")

        # Ejecutar el archivo pacientesPDF.py usando subprocess
        try:
            subprocess.run(["python", pacientes_pdf_path])
            print("Archivo pacientesPDF.py ejecutado con éxito.")
        except Exception as e:
            print("Error al ejecutar pacientesPDF.py:", e)

    def imprimir_medico(self):
        # Obtener la ruta completa al archivo medicosPDF.py
        current_dir = os.path.dirname(os.path.abspath(__file__))
        reportes_dir = os.path.join(current_dir, "..", "reportes")
        medico_pdf_path = os.path.join(reportes_dir, "MedicosPDF.py")

        # Ejecutar el archivo pacientesPDF.py usando subprocess
        try:
            subprocess.run(["python", medico_pdf_path])
            print("Archivo medicosPDF.py ejecutado con éxito.")
        except Exception as e:
            print("Error al ejecutar medicosPDF.py:", e)

    def on_row_press(self, instance_table, instance_row):
        print("Se presionó una fila:", instance_row)


    def on_check_press(self, instance_table, current_row):
        print("Se presionó el checkbox de la fila:", current_row)
        # Obtener las filas seleccionadas
        selected_rows = [row for row in self.data_table.get_row_checks()]
        if len(selected_rows) > 1:
            self.checkcomprobar = 2
            print("condicion mas de un check ", self.checkcomprobar)
        elif len(selected_rows) <= 0:
            self.checkcomprobar = 3
            print("No ha marcado nada ", self.checkcomprobar)
        elif len(selected_rows) == 1:
            print("Solo un checkbox seleccionado")
            self.checkcomprobar = 1
            self.globalselect = current_row
            print("condicion mas de un check ", self.checkcomprobar)
        else:
            self.checkcomprobar = 3

    def mostrar_pacientes(self):
        self.obtener_pacientes()

    def borrar(self):
        app = self.app
        if self.checkcomprobar == 1:
            id_paciente = self.globalselect[-1]
            url_paciente = f'http://localhost:9000/api/pacientes/{id_paciente}'
            response_paciente = requests.get(url_paciente)
            if response_paciente.status_code == 200:
                datapaciente = response_paciente.json()
                id_usuario = datapaciente["paciente_id"]["$oid"]
                fecha_actual = datetime.now()

                # Datos para eliminar al paciente
                dataeliminar = {
                    'cedula': datapaciente['cedula'],
                    'p_apellido': datapaciente["p_apellido"],
                    's_apellido': datapaciente["s_apellido"],
                    'p_nombre': datapaciente["p_nombre"],
                    's_nombre': datapaciente["s_nombre"],
                    't_sexo': datapaciente['t_sexo'],
                    't_sangre': datapaciente['t_sangre'],
                    'f_nacimiento': datapaciente["f_nacimiento"],
                    'n_telefono': datapaciente['n_telefono'],
                    # cambio
                    "id_usuario_eliminacion": "",
                    "fechaeliminacion": fecha_actual.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "created_at": fecha_actual.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "updated_at": fecha_actual.strftime("%Y-%m-%dT%H:%M:%SZ")
                }

                # Eliminar al paciente en la API
                response_delete_paciente = requests.delete(url_paciente)
                if response_delete_paciente.status_code == 200:
                    print("Paciente eliminado exitosamente")

                    # Obtener datos del usuario relacionado al médico
                    url_usuario = f'http://localhost:9000/api/users/{id_usuario}'
                    response_usuario = requests.get(url_usuario)
                    if response_usuario.status_code == 200:
                        datausuario = response_usuario.json()
                        data_usuario = {
                            "name": datausuario["name"],
                            "email": datausuario["email"],
                            "password": datausuario["password"],
                            "rol": 2,
                            "id_usuario_eliminacion": "",
                            "fechaeliminacion": fecha_actual.strftime("%Y-%m-%dT%H:%M:%SZ")
                        }
                        # Actualizar el usuario en la API con los datos de eliminación
                        response_update_usuario = requests.put(
                            url_usuario, json=data_usuario)
                        if response_update_usuario.status_code == 200:
                            self.load_table()
                            app.show_alert_dialog_eliminado()
                        else:
                            app.show_alert_dialog_eliminado()
                            print("Error al actualizar el usuario")
                    else:
                        app.show_alert_dialog_eliminado()
                        print("Error en búsqueda de usuario")
                else:
                    print("Error al eliminar al paciente")
            else:
                print("Error al obtener al paciente")
        elif self.checkcomprobar == 2:
            app.show_alert_dialog_varioscheck()
        elif self.checkcomprobar == 3:
            app.show_alert_dialog_noselectcheck()
        elif self.checkcomprobar == 5:
            app.show_alert_dialog_noselectcheck()
        else:
            print("Error")


#################################################
#            OBTENER DONACIONES
#################################################

    def obtener_donaciones(self):
            url_donaciones = 'http://localhost:5000/obtener_donaciones'
            response = requests.get(url_donaciones)

            if response.status_code == 200:
                donaciones = response.json()
                donacion_data = []
                for i, item in enumerate(donaciones, start=1):
                    if isinstance(item, dict):
                        row = (
                            f"{i}",
                            item['localidad'],
                            item['numero_bolsa'],
                            item['hemoglobina'],
                            item['volumen'],
                            item['fecha_hora'],
                            item['paciente_id'],
                        )
                        donacion_data.append(row)

                self.data_table = MDDataTable(
                    pos_hint={'center_y': 0.3, 'center_x': 0.5},
                    size_hint=(0.9, 0.5),
                    use_pagination=True,
                    elevation=1,
                    background_color_header="#F41F05",
                    column_data=[
                        ("No.", dp(30)),
                        ("Localidad", dp(50)),
                        ("Número de Bolsa", dp(30)),
                        ("Hemoglobina", dp(30)),
                        ("Volumen", dp(30)),
                        ("Fecha y Hora", dp(50)),
                        ("ID Paciente", dp(50)),
                    ],
                    row_data=donacion_data,
                )
                self.ids.admin_donaciones.add_widget(self.data_table)
                self.checkcomprobar = 5
            else:
                print("Error al obtener las donaciones")


#################################################
#            OBTENER MEDICOS
#################################################

    def obtener_medicos(self):
        urlmedicos = 'http://localhost:5000/obtener_medicos'
        response = requests.get(urlmedicos)

        if response.status_code == 200:
            medicos = response.json()
            medico_data = []
            for i, item in enumerate(medicos, start=1):
                if isinstance(item, dict):
                    row = (
                        f"{i}",  
                        item['cedula'],
                        item['nombre_completo'],
                        item['apellido_completo'],
                        item['fecha_nacimiento'],
                        item['sexo'],
                        item['tipo_sangre'],
                        item['telefono'],
                    )
                    medico_data.append(row)

            self.data_table = MDDataTable(
                pos_hint={'center_y': 0.4, 'center_x': 0.5},
                size_hint=(0.9, 0.5),
                use_pagination=True,
                elevation=1,
                background_color_header="#F41F05",
                column_data=[
                    ("No.", dp(30)),
                    ("Cédula", dp(30)),
                    ("Nombre", dp(30)),
                    ("Apellido", dp(30)),
                    ("Fecha Nacimiento", dp(30)),
                    ("Sexo", dp(30)),
                    ("Tipo Sangre", dp(30)),
                    ("Telefono", dp(30)),
                ],
                row_data=medico_data,
            )
            self.ids.anchor_medico.add_widget(self.data_table)
            self.checkcomprobar = 5
        else:
            print("Error al obtener los medicos")


#################################################
#            OBTENER AUDITORIA
#################################################
def obtener_auditorias(self):
        response = requests.get('http://localhost:5000/obtener_auditorias')  # Cambia la URL según tus necesidades
        datos_auditorias = response.json()
        print("Datos de auditorías recibidos desde el servidor:", datos_auditorias)
        self.auditorias_data = datos_auditorias

        if response.status_code == 200:
            auditoria_data = []
            for i, item in enumerate(self.auditorias_data, start=0):
                if isinstance(item, dict):
                    row = (
                        f"{i+1}",
                        item['fecha'],
                        item['usuario'],
                        item['accion'],
                    )
                    auditoria_data.append(row)

            self.data_table = MDDataTable(
                pos_hint={'center_y': 0.4, 'center_x': 0.5},
                size_hint=(0.9, 0.5),
                use_pagination=True,
                elevation=1,
                background_color_header="#F41F05",
                check=True,
                column_data=[
                    ("No.", dp(30)),
                    ("Fecha", dp(30)),
                    ("Usuario", dp(30)),
                    ("Acción", dp(30)),
                ],
                row_data=auditoria_data,
            )
            self.data_table.bind(on_row_press=self.on_row_press)
            self.data_table.bind(on_check_press=self.on_check_press)
            self.ids.audi.add_widget(self.data_table)
            self.checkcomprobar = 5
        else:
            print("Error al obtener las auditorías")