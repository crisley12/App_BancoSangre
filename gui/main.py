from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from kivymd.uix.label import MDLabel
from views.login_views import Login
from views.signup_views import Signup
from views.root_screen import RootScreen
from views.root_admin import RootAdmin
from views.root_medico import RootMedico
from screen.requirements_screen import RequirementsScreen
from screen.donate_screen import DonateScreen
from screen.paciente_basantranfs_screen import PacienteBasantranfsScreen
from screen.donaciones_screen import DonacionesScreen
from screen.questions_screen import QuestionsScreen
from conection import Database
from kivymd.uix.dialog import MDDialog
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.button import MDFlatButton
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
import re
import datetime
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, session, request, jsonify
Window.size = (350, 600)


class MainApp(MDApp):
    paciente_id = None
    data = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database(database_name='banco_de_sangre')

    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("views_kv/main.kv"))
        screen_manager.add_widget(Login(name='login'))
        screen_manager.add_widget(Signup(name='signup'))
        screen_manager.add_widget(RootScreen(name='root'))
        screen_manager.add_widget(RootAdmin(name='root_admin'))
        screen_manager.add_widget(RootMedico(name='root_medico'))
        screen_manager.add_widget(RequirementsScreen(name='requirements'))
        screen_manager.add_widget(DonateScreen(name='donate'))
        screen_manager.add_widget(DonacionesScreen(name='paciente_donaciones'))
        screen_manager.add_widget(
            PacienteBasantranfsScreen(name='paciente_basantranfs'))
        screen_manager.add_widget(QuestionsScreen(name='questions'))

        return screen_manager

    def on_start(self):
        Clock.schedule_once(self.login_inicio, 5)

    def login_inicio(self, *args):
        screen_manager.current = 'login'



    def validar_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    def solo_numeros(self, text, mensaje_numero):
        if text.isdigit():
            mensaje_numero.opacity = 0
            return text
        else:
            mensaje_numero.opacity = 1
            return ""

    def solo_letras(self, text, mensaje_nombre):
        if text.isalpha():
            mensaje_nombre.opacity = 0
            return text
        else:
            mensaje_nombre.opacity = 1
            return ""

    def validar_cedula_venezolana(self, cedula):
        if not cedula.isdigit() or len(cedula) != 8:
            return False
        return True

    def validar_telefono(self, telefono):
        if not telefono.isdigit() or len(telefono) != 11:
            return False
        return True

    def validar_comtraseña(self, contraseña):
        if len(contraseña) > 16 or len(contraseña) < 8:
            return False
        return True

    def on_text(self, instance, value):
        if value == "":
            self.helper_text = "dd/mm/yyyy"
        else:
            self.helper_text = ""

    def validate_date(self, text):
        parts = text.split('/')
        if len(parts) == 3 and all(part.isdigit() for part in parts):
            day, month, year = map(int, parts)
            if 1 <= day <= 31 and 1 <= month <= 12:
                current_year = datetime.datetime.now().year
                age = current_year - year
                if age >= 18:
                    return True
                else:
                    return "No eres mayor de edad."
            else:
                return "Fecha de nacimiento inválida."
        else:
            return "Formato de fecha de nacimiento incorrecto (dd/mm/yyyy)."

    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="Cerrar", on_release=lambda *args: dialog.dismiss()
                )
            ],
        )
        dialog.open()

    #################################################
    #            VALIDACION LOGIN
    #################################################

    def validacionUser(self):
        login_screen = screen_manager.get_screen('login')
        username = login_screen.ids.email.text
        self.validar_email(username)
        if not self.validar_email(username):
            self.show_dialog("Error", "Ingrese un email válido")
            return

        password = login_screen.ids.password.text
        if not username or not password:
            self.show_dialog("Error", "Por favor, complete todos los campos.")
            return

        self.data = {
            "email": username,
            "password": password
        }
        self.login()


    def login(self):
        response = requests.post("http://localhost:5000/login", json=self.data)
        print(response)

        if response.status_code == 200:
            self.show_dialog("Bienvenido", "¡Bienvenido!")
            user_data = response.json()
            role = user_data.get('role')
            if role == 'paciente':
                screen_manager.current = 'root'
            elif role == 'medico':
                screen_manager.current = 'root_medico'

            elif role == 'admin':
                screen_manager.current = 'root_admin'

            else:
                self.show_dialog("Error", "Rol no reconocido.")
                return

            # Obtener el user_id del usuario actual de la respuesta JSON
            user_id = response.json().get('user_id')

            # Obtener el paciente_id del usuario actual de la sesión
            self.paciente_id = response.json().get('paciente_id')

            print("El user_id del usuario actual es:", user_id)
            print("El paciente_id del usuario actual es:", self.paciente_id)

            self.current_user_id = user_id

    def logout(self):
        url_logout = 'http://localhost:5000/logout'
        user_id = self.current_user_id  

        if not user_id:
            print("No hay usuario para cerrar sesión.")
            return

        try:
            response = requests.post(url_logout, data={'user_id': user_id})

            if response.status_code == 200:
                print("Sesión cerrada exitosamente")
                self.root.current = 'login'  

            else:
                print("Error al cerrar la sesión")

        except requests.exceptions.RequestException as e:
            print("Error al comunicarse con la API")

#################################################
#            PANTALLA PACIENTE
#################################################

            # Obtener los datos del paciente si están disponibles
            paciente = response.json().get('paciente')
            if paciente:
                nombre_paciente = paciente.get('nombre')
                apellido_paciente = paciente.get('apellido')
                tipo_sangre_paciente = paciente.get('tipo_sangre')

            # Obtener la pantalla root
                root_screen = screen_manager.get_screen('root')
                root_screen.ids.nombre_user_paciente.text = f"{nombre_paciente} {apellido_paciente}"
                root_screen.ids.sagre_user_paciente.text = (
                    tipo_sangre_paciente)
                root_screen.ids.sagre_sangre_paciente.text = (
                    tipo_sangre_paciente)
                print("Nombre del paciente:", nombre_paciente)
                print("Nombre del paciente:", apellido_paciente)
                print("Tipo de sangre del paciente:", tipo_sangre_paciente)

                datos_tipo_sangre = {
                    'A+': {'donar': ['A+', 'AB+'], 'recibir': ['A+', 'A-', 'O+', 'O-']},
                    'A-': {'donar': ['A+', 'A-', 'AB+', 'AB-'], 'recibir': ['A-', 'O-']},
                    'B+': {'donar': ['B+', 'AB+'], 'recibir': ['B+', 'B-', 'O+', 'O-']},
                    'B-': {'donar': ['B+', 'B-', 'AB+', 'AB-'], 'recibir': ['B-', 'O-']},
                    'AB+': {'donar': ['AB+'], 'recibir': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']},
                    'AB-': {'donar': ['AB+', 'AB-'], 'recibir': ['A-', 'B-', 'AB-', 'O-']},
                    'O+': {'donar': ['A+', 'B+', 'AB+', 'O+'], 'recibir': ['O+', 'O-']},
                    'O-': {'donar': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'], 'recibir': ['O-']}
                }

                # Obtener la información de tipo sangre y recepción del paciente
                datos_paciente_sangre = datos_tipo_sangre.get(
                    tipo_sangre_paciente, {'donar': [], 'recibir': []})

                # Mostrar la compatibilidad en los widgets correspondientes
                root_screen.ids.paciente_donar.text = '  '.join(
                    datos_paciente_sangre['donar'])
                root_screen.ids.paciente_recibir.text = '  '.join(
                    datos_paciente_sangre['recibir'])
                self.obtener_donaciones_paciente()
        else:
            self.show_dialog("Error", "Usuario o contraseña incorrecto.")


#################################################
#             DONACIONES POR PACIENTE
#################################################


    def obtener_donaciones_paciente(self):
        donaciones_response = requests.get(
            f"http://localhost:5000/donaciones_paciente?paciente_id={self.paciente_id}")
        print("primer dato", donaciones_response)

        if donaciones_response.status_code == 200:
            donaciones = donaciones_response.json()

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
                    donante_hemoglobina = item['hemoglobina']
                    print(donacion_data)

            if donacion_data:  # Verifica si hay donaciones en la lista
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
                donaciones_paciente = screen_manager.get_screen(
                    'paciente_donaciones')
                donaciones_paciente.ids.donaciones.clear_widgets()
                donaciones_paciente.ids.donaciones.add_widget(self.data_table)

                root_screen = screen_manager.get_screen('root')
                root_screen.ids.donante_hemoglobina.text = donante_hemoglobina
            else:
                mensaje = MDLabel(
                    text="No se encontraron donaciones",
                    halign="center",
                    theme_text_color="Custom",
                    text_color='red',
                    font_style="H5"
                )
                donaciones_paciente = screen_manager.get_screen(
                    'paciente_donaciones')
                donaciones_paciente.ids.donaciones.add_widget(mensaje)

        else:
            self.show_dialog("Error", "Error al obtener las donaciones")


#################################################
#            VALIDACION REGISTRO
#################################################


    def RegistroPaciente(self):
        registre_screen = screen_manager.get_screen('signup')
        cedula = registre_screen.ids.cedula.text
        p_apellido = registre_screen.ids.p_apellido.text
        s_apellido = registre_screen.ids.s_apellido.text
        p_nombre = registre_screen.ids.p_nombre.text
        s_nombre = registre_screen.ids.s_nombre.text
        n_telefono = registre_screen.ids.n_telefono.text
        t_sangre = registre_screen.ids.t_sangre.text
        t_sexo = registre_screen.ids.t_sexo.text
        f_nacimiento = registre_screen.ids.f_nacimiento.text
        email = registre_screen.ids.email.text
        password = registre_screen.ids.password.text

        if not self.validar_cedula_venezolana(cedula):
            self.show_dialog("Error", "Formato de cédula incorrecto")
            return

        if not self.validar_telefono(n_telefono):
            self.show_dialog(
                "Error", "Formato de número de teléfono incorrecto")
            return

        if not self.validar_comtraseña(password):
            self.show_dialog(
                "Error", "La contraseña debe tener entre 8 y 16 caracteres")
            return

        if not self.validar_email(email):
            self.show_dialog(
                "Error", "Por favor, ingrese un correo electrónico válido.")
            return

        date_validation_result = self.validate_date(f_nacimiento)
        if date_validation_result != True:
            self.show_dialog("Error", date_validation_result)
            return

        try:
            # Convertir la fecha de nacimiento a un objeto de tipo datetime
            f_nacimiento_dt = datetime.datetime.strptime(
                f_nacimiento, '%d/%m/%Y').date()
        except ValueError:
            self.show_dialog(
                "Error", "Formato de fecha de nacimiento incorrecto (dd/mm/yyyy).")
            return

        # Validar que la fecha de nacimiento sea anterior a la fecha actual
        if f_nacimiento_dt >= datetime.date.today():
            self.show_dialog("Error", "Fecha de nacimiento inválida.")
            return

        # Verificar si los campos están vacíos
        campo_vacio = []
        if not cedula:
            campo_vacio.append("cedula")
        if not p_apellido:
            campo_vacio.append("primer apellido")
        if not s_apellido:
            campo_vacio.append("segundo apellido")
        if not p_nombre:
            campo_vacio.append("primer nombre")
        if not s_nombre:
            campo_vacio.append("segundo nombre")
        if not n_telefono:
            campo_vacio.append("numero de telefono")
        if not t_sangre:
            campo_vacio.append("tipo de sangre")
        if not t_sexo:
            campo_vacio.append("tipo de sexo")
        if not f_nacimiento:
            campo_vacio.append("fecha de nacimiento")
        if not email:
            campo_vacio.append("email")
        if not password:
            campo_vacio.append("password")

        if campo_vacio:
            campos_str = ", ".join(campo_vacio)
            mensaje = f"Por favor, complete los siguientes campos: {campos_str}"
            self.show_dialog("Error", mensaje)
            return

        # Insertar el paciente en la colección "pacientes"
        data = {
            'cedula': cedula,
            'p_apellido': p_apellido,
            's_apellido': s_apellido,
            'p_nombre': p_nombre,
            's_nombre': s_nombre,
            'n_telefono': n_telefono,
            't_sangre': t_sangre,
            't_sexo': t_sexo,
            'f_nacimiento': f_nacimiento,
            'email': email,
            'password': password
        }

        response = requests.post(
            'http://localhost:5000/registro_paciente', json=data)
        if response.status_code == 201:
            self.show_dialog("Registro exitoso!",
                             "¡El registro ha sido exitoso!")
            screen_manager.current = "login"
        elif response.status_code == 409:
            self.show_dialog("Error", "Paciente ya existe.")
        else:
            self.show_dialog("Error", "Error al registrar")

    def RegistroMedico(self):
        registre_screen = screen_manager.get_screen('root_admin')
        cedula = registre_screen.ids.cedula_medico.text
        p_apellido = registre_screen.ids.p_apellido_medico.text
        s_apellido = registre_screen.ids.s_apellido_medico.text
        p_nombre = registre_screen.ids.p_nombre_medico.text
        s_nombre = registre_screen.ids.s_nombre_medico.text
        n_telefono = registre_screen.ids.n_telefono_medico.text
        t_sangre = registre_screen.ids.t_sangre_medico.text
        t_sexo = registre_screen.ids.t_sexo_medico.text
        f_nacimiento = registre_screen.ids.f_nacimiento_medico.text
        email = registre_screen.ids.email_medico.text
        password = registre_screen.ids.password_medico.text

        if not self.validar_cedula_venezolana(cedula):
            self.show_dialog("Error", "Formato de cédula incorrecto")
            return

        if not self.validar_telefono(n_telefono):
            self.show_dialog(
                "Error", "Formato de número de teléfono incorrecto")
            return

        if not self.validar_comtraseña(password):
            self.show_dialog(
                "Error", "La contraseña debe tener entre 8 y 16 caracteres")
            return

        if not self.validar_email(email):
            self.show_dialog(
                "Error", "Por favor, ingrese un correo electrónico válido.")
            return

        campo_vacio = []
        if not cedula:
            campo_vacio.append("cedula")
        if not p_apellido:
            campo_vacio.append("primer apellido")
        if not s_apellido:
            campo_vacio.append("segundo apellido")
        if not p_nombre:
            campo_vacio.append("primer nombre")
        if not s_nombre:
            campo_vacio.append("segundo nombre")
        if not n_telefono:
            campo_vacio.append("numero de telefono")
        if not t_sangre:
            campo_vacio.append("tipo de sangre")
        if not t_sexo:
            campo_vacio.append("tipo de sexo")
        if not f_nacimiento:
            campo_vacio.append("fecha de nacimiento")
        if not email:
            campo_vacio.append("email")
        if not password:
            campo_vacio.append("password")

        if campo_vacio:
            campos_str = ", ".join(campo_vacio)
            mensaje = f"Por favor, complete los siguientes campos: {campos_str}"
            self.show_dialog("Error", mensaje)
            return

        date_validation_result = self.validate_date(f_nacimiento)
        if date_validation_result != True:
            self.show_dialog("Error", date_validation_result)
            return

        try:
            f_nacimiento_dt = datetime.datetime.strptime(
                f_nacimiento, '%d/%m/%Y').date()
        except ValueError:
            self.show_dialog(
                "Error", "Formato de fecha de nacimiento incorrecto (dd/mm/yyyy).")
            return

        if f_nacimiento_dt >= datetime.date.today():
            self.show_dialog("Error", "Fecha de nacimiento inválida.")
            return

        data = {
            'cedula': cedula,
            'p_apellido': p_apellido,
            's_apellido': s_apellido,
            'p_nombre': p_nombre,
            's_nombre': s_nombre,
            'n_telefono': n_telefono,
            't_sangre': t_sangre,
            't_sexo': t_sexo,
            'f_nacimiento': f_nacimiento,
            'email': email,
            'password': password
        }

        response = requests.post(
            'http://localhost:5000/registro_medico', json=data)
        if response.status_code == 201:
            self.show_dialog("Registro exitoso!",
                             "¡El registro ha sido exitoso!")
            # screen_manager.current = "root_admin"
        elif response.status_code == 409:
            self.show_dialog("Error", "El Medico ya existe.")
        else:
            self.show_dialog("Error", "Error al registrar")

    def RegistroAdmin(self):
        registre_screen = screen_manager.get_screen('root_admin')
        p_nombre = registre_screen.ids.p_nombre_admin.text
        email = registre_screen.ids.email_admin.text
        password = registre_screen.ids.password_admin.text

        if not self.validar_email(email):
            self.show_dialog(
                "Error", "Por favor, ingrese un correo electrónico válido.")
            return

        if not self.validar_comtraseña(password):
            self.show_dialog(
                "Error", "La contraseña debe tener entre 8 y 16 caracteres")
            return

        campo_vacio = []
        if not p_nombre:
            campo_vacio.append("primer nombre")
        if not email:
            campo_vacio.append("email")
        if not password:
            campo_vacio.append("password")

        if campo_vacio:
            campos_str = ", ".join(campo_vacio)
            mensaje = f"Por favor, complete los siguientes campos: {campos_str}"
            self.show_dialog("Error", mensaje)
            return

        data = {
            'p_nombre': p_nombre,
            'email': email,
            'password': password
        }

        response = requests.post(
            'http://localhost:5000/registro_admin', json=data)
        if response.status_code == 201:
            self.show_dialog("Registro exitoso!",
                             "¡El registro ha sido exitoso!")
            # root_screen = screen_manager.get_screen('root')
            # root_screen.ids.donante_hemoglobina.text = donante_hemoglobina
            # screen_manager.current = "root_admin"
        elif response.status_code == 409:
            self.show_dialog("Error", "El Administrador ya existe.")
        else:
            self.show_dialog("Error", "Error al registrar")


if __name__ == '__main__':
    MainApp().run()
