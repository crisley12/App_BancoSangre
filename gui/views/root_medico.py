from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.datatables import MDDataTable
from datetime import datetime
from kivy.metrics import dp
import requests


class MostrarDonaciones(MDScreen):
    pass


class CrearDonacion(MDScreen):
    pass


class BuscarPacientes(MDScreen):
    pass


class CrearPaciente(MDScreen):
    pass


class MostrarPacientesMedico(MDScreen):
    pass


class ContentNavigationDrawerMedico(MDScrollView):
    screen = ObjectProperty()
    nav = ObjectProperty()
    root_medico_instance = None


class RootMedico(MDScreen):
    data_table = ObjectProperty(None)
    globalselect = []
    checkcomprobar = 5
    paciente_id = None

    def __init__(self, **kwargs) -> None:
        Builder.load_file('views_kv/root_medico.kv')
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        ContentNavigationDrawerMedico.root_medico_instance = self
        self.create_dropdown1()
        self.create_dropdown2()


#################################################
#            INPUT CEDULA
#################################################

    Max_c = 8

    def check_length_cedula_buscar(self):
        cedula_buscar = self.ids.cedula_buscar
        text = cedula_buscar.text
        if len(text) > self.Max_c:
            cedula_buscar.foreground_color = 1, 0, 0, 1
        else:
            cedula_buscar.foreground_color = 0, 0, 0, 1


#################################################
#            Buscar Pacientes
#################################################


    def buscarPacientes(self):
        app = self.app
        buscar_cedula = self.ids.cedula_buscar.text
        if not buscar_cedula:
            app.show_dialog("Error", "Por favor, ingrese una cédula.")
            return
        if not app.validar_cedula_venezolana(buscar_cedula):
            app.show_dialog("Error", "Formato de cédula incorrecto")
            return

        url_api = 'http://localhost:5000/buscar_pacientes_por_cedula'
        data = {
            "cedula": buscar_cedula
        }

        response = requests.post(url_api, json=data)

        if response.status_code == 200:
            paciente = response.json()
            if paciente:
                paciente_id = paciente.get('paciente_id')
                cedula = paciente.get('cedula')
                nombre = paciente.get('p_nombre')
                apellido = paciente.get('p_apellido')

                app.show_dialog(
                    "Paciente encontrado", f"Cedula: {cedula}   Paciente: {nombre} {apellido}")
                self.ids.screen.current = "crear_donacion"
                self.paciente_id = paciente_id

            else:
                app.show_dialog(
                    "Error", "No se encontró ningún paciente con esa cédula.")
        else:
            app.show_dialog("Error", "El paciente no exixte")
            self.ids.screen.current = "crear_paciente"

    def guardarDonacion(self):
        app = self.app
        localidad = self.ids.banco.text
        numero_bolsa = self.ids.bolsa.text
        hemoglobina = self.ids.hemoglobina.text
        volumen = self.ids.volumen.text

        try:
            if not hemoglobina.endswith('g/dL'):
                hemoglobina += ' g/dL'

            hemoglobina_value = float(hemoglobina[:-5])

            if hemoglobina_value < 10.0 or hemoglobina_value > 20.0:
                app.show_dialog(
                    "Error", "El valor de hemoglobina debe estar entre 10.0 y 20.0 g/dL.")
                return

            if not volumen.endswith('ml'):
                volumen += ' ml'

            volumen_value = float(volumen[:-2])

            if volumen_value < 250.0 or volumen_value > 500.0:
                app.show_dialog(
                    "Error", "El volumen de la bolsa debe estar entre 250.0 y 500.0 mL.")
                return

        except ValueError as e:
            app.show_dialog("Error", str(e))
            return

        if not self.paciente_id:
            app.show_dialog(
                "Error", "Primero debe buscar y seleccionar un paciente.")
            return

        # Obtener la fecha y hora actual
        fecha_hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Obtener el ID del paciente encontrado
        paciente_id = self.paciente_id

        datos_donacion = {
            "localidad": localidad,
            "numero_bolsa": numero_bolsa,
            "hemoglobina": hemoglobina,
            "volumen": volumen,
            "fecha_hora": fecha_hora_actual,
            "paciente_id": paciente_id
        }

        url_api_donaciones = 'http://localhost:5000/crear_donacion'
        response_donacion = requests.post(
            url_api_donaciones, json=datos_donacion)

        if response_donacion.status_code == 200:
            app.show_dialog("Donación guardada",
                            "La donación se ha registrado exitosamente.")
            self.ids.screen.current = "donaciones"

        else:
            app.show_dialog(
                "Error", "Error al guardar la donación. Intente nuevamente.")


#################################################
#            MOSTRAR DONACIONES
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
                check=True,
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
            self.data_table.bind(on_row_press=self.on_row_press)
            self.data_table.bind(on_check_press=self.on_check_press)
            self.ids.anchor_layout_donaciones.add_widget(self.data_table)
            self.checkcomprobar = 5
        else:
            print("Error al obtener las donaciones")

    def mostrar_donaciones(self):
        self.obtener_donaciones()


#################################################
#            MOSTRAR PACIENTES
#################################################


    def obtener_pacientes(self):
        urlpacientes = 'http://localhost:5000/obtener_pacientes'
        response = requests.get(urlpacientes)

        if response.status_code == 200:
            pacientes = response.json()
            paciente_data = []
            for i, item in enumerate(pacientes, start=1):
                if isinstance(item, dict):
                    row = (
                        # Obtener el valor correspondiente a cada columna en la fila
                        f"{i}",  # Número como cadena
                        item['cedula'],
                        item['nombre_completo'],
                        item['apellido_completo'],
                        item['fecha_nacimiento'],
                        item['sexo'],
                        item['tipo_sangre'],
                        item['telefono'],
                        item['paciente_id']
                    )
                    # Agregar la fila a la lista de datos de filas
                    paciente_data.append(row)

            # Crear el MDDataTable con los datos obtenidos
            self.data_table = MDDataTable(
                pos_hint={'center_y': 0.3, 'center_x': 0.5},
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
                    ("ID Paciente", dp(50)),
                ],
                row_data=paciente_data,  # Pasar la lista de datos de filas al MDDataTable
            )
            self.data_table.bind(on_row_press=self.on_row_press)
            self.data_table.bind(on_check_press=self.on_check_press)
            # Agregar el MDDataTable al layout
            self.ids.anchor_layout_pacientes.add_widget(self.data_table)
            self.checkcomprobar = 5
        else:
            print("Error al obtener los pacientes")

    def on_row_press(self, instance_table, instance_row):
        print("Se presionó una fila:", instance_row)

    def on_check_press(self, instance_table, current_row):
        print("Se presionó el checkbox de la fila:", current_row)
        # Obtener las filas seleccionadas
        selected_rows = [row for row in self.data_tables.get_row_checks()]
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

    def create_dropdown1(self):

        items_1 = ['F', 'M']

        sexo_items = [
            {
                "viewclass": "OneLineListItem",
                "height": dp(30),
                "text": f"{i}",
                "on_release": lambda x=f"{i}": self.set_item1(x),
            } for i in items_1]
        self.sexo = MDDropdownMenu(
            caller=self.ids.t_sexo,
            items=sexo_items,
            position="bottom",
            width_mult=1,
            background_color=[1, 1, 1, 1],
            elevation=2
        )

    def set_item1(self, text__item):
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
                "on_release": lambda x=f"{i}": self.set_item2(x),
            } for i in items_2]
        self.sangre = MDDropdownMenu(
            caller=self.ids.t_sangre,
            items=sangre_items,
            position="bottom",
            width_mult=1.5,
            background_color=[1, 1, 1, 1],
            elevation=2
        )

    def set_item2(self, text__item):
        self.ids.t_sangre.text = text__item
        self.sangre.dismiss()


#################################################
#            INPUT CEDULA
#################################################

    Max_c = 8

    def check_length_cedula(self):
        cedula = self.ids.cedula
        text = cedula.text
        if len(text) > self.Max_c:
            cedula.foreground_color = 1, 0, 0, 1
        else:
            cedula.foreground_color = 0, 0, 0, 1


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
