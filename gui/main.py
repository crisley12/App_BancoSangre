from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from views.login_views import Login
from views.signup_views import Signup
from views.root_screen import RootScreen
from screen.requirements_screen import RequirementsScreen
from screen.donate_screen import DonateScreen
from screen.paciente_basantranfs_screen import PacienteBasantranfsScreen
from screen.need_donate_screen import NeedDonateScreen
from screen.process_screen import ProcessScreen
from screen.questions_screen import QuestionsScreen
from screen.about_screen import AboutScreen
from conection import Database
from kivymd.uix.dialog import MDDialog
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.button import MDFlatButton
import re
import datetime
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, session, request, jsonify
Window.size = (350, 600)


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database(database_name='banco_de_sangre')

    # Constructor de la interfaz
    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("views_kv/main.kv"))
        screen_manager.add_widget(Login(name='login'))
        screen_manager.add_widget(Signup(name='signup'))
        screen_manager.add_widget(RootScreen(name='root'))
        screen_manager.add_widget(RequirementsScreen(name='requirements'))
        screen_manager.add_widget(DonateScreen(name='donate'))
        screen_manager.add_widget(PacienteBasantranfsScreen(name='paciente_basantranfs'))

        '''
        screen_manager.add_widget(NeedDonateScreen(name='need'))
        screen_manager.add_widget(ProcessScreen(name='process'))
        screen_manager.add_widget(QuestionsScreen(name='questions'))
        screen_manager.add_widget(AboutScreen(name='about'))
        '''

        '''
        directory = "gui/root_screen.py"  # Reemplazar con la ruta correcta
        root_screen = RootScreen(directory, name='root')
        screen_manager.add_widget(root_screen)
         Cargar los archivos KV
        self.load_all_kv_files(self.directory)

        Retornar RootScreen() o usar screen_manager como raíz si es necesario
        return RootScreen()
        '''
        return screen_manager

    # Transicion de pantalla de inicio a --> LoginScreen
    def on_start(self):
        Clock.schedule_once(self.login, 3)

    def login(self, *args):
        screen_manager.current = 'donate'

    #################################################
    #            VALIDACION LOGIN
    #################################################

    def validacionUser(self):
        # Obtener el texto de los campos de usuario y contraseña
        login_screen = screen_manager.get_screen('login')
        username = login_screen.ids.email.text  # .strip()
        self.validar_email(username)
        if not self.validar_email(username):
            self.show_dialog("Error", "Ingrese un email válido")
            return
        password = login_screen.ids.password.text  # .strip()

        # Verificar si los campos están vacíos
        if not username or not password:
            self.show_dialog("Error", "Por favor, complete todos los campos.")
            return
# Realizar la solicitud de inicio de sesión a la API
        import requests

        data = {
            "email": username,
            "password": password
        }

        response = requests.post("http://localhost:5000/login", json=data)
        print(response)

        if response.status_code == 200:
            self.show_dialog("Bienvenido", "¡Bienvenido!")
            screen_manager.current = "root"

            # Obtener el user_id del usuario actual de la respuesta JSON
            user_id = response.json().get('user_id')

            print("El user_id del usuario actual es:", user_id)

            # Obtener la colección de usuarios
            # users_collection = self.db.get_collection('users')

            # Buscar al usuario en la base de datos
            # user = users_collection.find_one({'email': username, 'password': password})

            # Verificar si el usuario fue encontrado o no
            # if user is not None:
            #    self.show_dialog("Error", "Usuario o contraseña incorrecto.")

            # return jsonify(response), 200

        else:
            self.show_dialog("Error", "Usuario o contraseña incorrecto.")

    def request_error(req, error):
        print("Error en la solicitud:", error)
    #################################################
    #            VALIDACION REGISTRO
    #################################################

    # Validar el formato del email
    def validar_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    # Valida solo números
    def solo_numeros(self, text, mensaje_numero):
        if text.isdigit():
            mensaje_numero.opacity = 0
            return text
        else:
            mensaje_numero.opacity = 1
            return ""

    # Valida solo letras
    def solo_letras(self, text, mensaje_nombre):
        if text.isalpha():
            mensaje_nombre.opacity = 0
            return text
        else:
            mensaje_nombre.opacity = 1
            return ""

    # Valida el formato de fecha
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

    def validacionRegistro(self):
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

        # Validar el formato del email
        if not self.validar_email(email):
            self.show_dialog(
                "Error", "Por favor, ingrese un correo electrónico válido.")
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

         # Validar la fecha de nacimiento
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

        response = requests.post('http://localhost:5000/registro', json=data)
        if response.status_code == 201:
            self.show_dialog("Registro exitoso!")
            screen_manager.current = "login"
        elif response.status_code == 409:
            self.show_dialog("Error", "Paciente ya existe.")
        else:
            self.show_dialog("Error", "Error al registrar")

    def show_dialog(self, title, text):
        # Crear y mostrar un cuadro de diálogo
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
 #       PANTALLAS DE ROOT
#################################################

    # Obtener la instancia de la pantalla MenuScreen desde RootScreen
        # group_blood_screen = root.ids.group_blood_screen

        # Acceder a los IDs de los widgets en MenuScreen
        # menu_button = group_blood_screen.ids.
        # menu_label = group_blood_screen.ids.title

        # Realizar acciones con los widgets según los datos de la base de datos
        # Por ejemplo, agregar un nuevo widget según los datos de la base de datos
        # new_widget = CustomWidget()
        # group_blood_screen.add_widget(new_widget)


if __name__ == '__main__':
    MainApp().run()
