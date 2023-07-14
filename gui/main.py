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
        screen_manager.current = 'login'

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

        import requests

        data = {
            "email": username,
            "password": password
        }

        url = 'http://localhost:9000/api/users/'
        response = requests.get(url, params=data)

        if response.status_code == 200:
            user = response.json()
            print("este es el usuario", user)
            print("este es el id_usuario", user["_id"])
            id_usuario = user["_id"]
        else:
            print("Error al obtener el usuario. Código de estado:",
                  response.status_code)
            # busquedapaciente
            # def busquedapaciente(id_usuario):
            # print("la cedula buscada es:", id_usuario)
        url = f'http://localhost:9000/api/pacientes/{id_usuario}'
        req = UrlRequest(url, on_success=lambda req, result: self.request_success(
            req, result, id_usuario), on_error=self.request_error)

    def request_success(self, req, result, id_usuario):
        if result is None:
            print("No se encontraron datos", id_usuario)
            # app.show_alert_dialog(cedula_str)
            return
        if len(result) >= 1:
            print("Si encontro", result)
            self.show_dialog(f"Bienvenido! {str(result)}")
            screen_manager.current = 'root'
            # app.show_alert_dialog_cita(cedula_str)
        else:
            print("no")

    def request_error(req, error):
        print("Error en la solicitud:", error)
    #################################################
    #            VALIDACION REGISTRO
    #################################################

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
            # f_nacimiento_formateada = f_nacimiento.strftime("%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            self.show_dialog(
                "Error", "Formato de fecha de nacimiento incorrecto (dd/mm/yyyy).")
            return

        # Validar que la fecha de nacimiento sea anterior a la fecha actual
        if f_nacimiento_dt >= datetime.date.today():
            self.show_dialog("Error", "Fecha de nacimiento inválida.")
            return

        # url = 'http://localhost:5000/registro'
        # data = {
        #     'cedula': cedula,
        #     'p_apellido': p_apellido,
        #     's_apellido': s_apellido,
        #     'p_nombre': p_nombre,
        #     's_nombre': s_nombre,
        #     'n_telefono': n_telefono,
        #     't_sangre': t_sangre,
        #     't_sexo': t_sexo,
        #     'f_nacimiento': f_nacimiento,
        #     'email': email,
        #     'password': password
        # }

        email_str = str(email)
        password_str = str(password)
        cedula_str = str(cedula)
        p_apellido_str = str(p_apellido)
        s_apellido_str = str(s_apellido)
        p_nombre_str = str(p_nombre)
        s_nombre_str = str(s_nombre)
        n_telefono_str = str(n_telefono)
        t_sangre_str = str(t_sangre)
        t_sexo_str = str(t_sexo)
        f_nacimiento_str = str(f_nacimiento)

        url3 = f'http://localhost:9000/api/pacientes/cedula/{cedula_str}'
        response3 = requests.get(url3)

        if response3.status_code == 200:
            paciente = response3.json()

            if paciente.get("message") != "Paciente no encontrado":
                print("Alerta: Ya existe un paciente con esta cédula")
                print(paciente)
                self.show_dialog("Ya existe la cedula", "Verifica")
            else:
                print("Alerta: NO existe un paciente con esta cédula")
                print(paciente)
                self.create_paciente_users(email_str, password_str, cedula_str, p_apellido_str, s_apellido_str,
                                           p_nombre_str, s_nombre_str, n_telefono_str, t_sangre_str, t_sexo_str, f_nacimiento_str)

        else:
            print("Error en la solicitud:", response3.status_code)

    def create_paciente_users(self, email_str, password_str, cedula_str, p_apellido_str, s_apellido_str, p_nombre_str, s_nombre_str, n_telefono_str, t_sangre_str, t_sexo_str, f_nacimiento_str):
        url1 = 'http://localhost:9000/api/users'
        data1 = {
            'email': email_str,
            'password': password_str,
            'rol_id': 2
        }
        response = requests.post(url1, json=data1)
        response_data = response.json()
        id_usuario = response_data['_id']
        id_usuario_str = str(id_usuario)

        url2 = 'http://localhost:9000/api/pacientes'
        data = {
            'cedula': cedula_str,
            'p_apellido': p_apellido_str,
            's_apellido': s_apellido_str,
            'p_nombre': p_nombre_str,
            's_nombre': s_nombre_str,
            'n_telefono': n_telefono_str,
            't_sangre': t_sangre_str,
            't_sexo': t_sexo_str,
            'f_nacimiento': f_nacimiento_str,
            'user_id': id_usuario_str
        }
        response = requests.post(url2, json=data)

        if response.status_code == 200:
            self.show_dialog("Registro exitoso", "¡Registro exitoso!")
            screen_manager.current = "login"
        elif response.status_code == 409:
            self.show_dialog("Error", "El paciente ya existe.")
        else:
            error_message = response.json().get("message", "Error al registrar.")
            self.show_dialog("Error", error_message)
            
    # def request_success(self, req, result):
    #     if result is None:
    #         print("No se encontraron datos")
    #         # app.show_alert_dialog(cedula_str)
    #         return
    #     if len(result) >= 1:
    #         print("Si encontro")
    #         print("Si encontro", result)
    #         url2 = f'http://localhost:9000/api/pacientes'
    #     response = requests.get(url2)
    #     if response.status_code == 200:
    #         pacientes = response.json()

    #         # Encontrar el valor máximo de nhistoria_paciente
    #         max_nhistoria = max(paciente['nhistoria_paciente'] for paciente in pacientes)
    #         idmaximo = max(paciente['idpaciente'] for paciente in pacientes)

    #         max_nhistoriasuma = str(max_nhistoria + 1)
    #         idmaximosuma = str(idmaximo + 1)
    #         # app.show_alert_dialog_cita(cedula_str)
    #     else:
    #         print("no")

    # def request_error(req, error):
    #     print("Error en la solicitud:", error)

        # if response.status_code == 200:
        #     app.show_alert_dialog_registradoconexito()
        # else:
        #     print("Ocurrió un error en la solicitud")

        # response = requests.post('http://localhost:5000/registro', json=data)

        '''# Obtener la colección de pacientes
        pacientes_collection = self.db.get_collection('pacientes')

        # Verificar si el paciente ya existe en la base de datos
        existing_paciente = pacientes_collection.find_one({'cedula': cedula})
        if existing_paciente:
            self.show_dialog("Error", "El paciente ya existe.")
        else:
            try:
                # Insertar el paciente en la colección "pacientes"
                paciente_id = pacientes_collection.insert_one({
                    'cedula': cedula,
                    'p_apellido': p_apellido,
                    's_apellido': s_apellido,
                    'p_nombre': p_nombre,
                    's_nombre': s_nombre,
                    'n_telefono': n_telefono,
                    't_sangre': t_sangre,
                    't_sexo': t_sexo,
                    'f_nacimiento': f_nacimiento
                }).inserted_id

                if paciente_id:
                    # Obtener la colección de roles
                    roles_collection = self.db.get_collection('roles')

                    # Buscar el rol "paciente"
                    paciente_role = roles_collection.find_one(
                        {'nombre': 'paciente'})

                    if not paciente_role:
                        # Si el rol "paciente" no existe, se crea
                        paciente_role_id = roles_collection.insert_one(
                            {'nombre': 'paciente'}).inserted_id
                    else:
                        paciente_role_id = paciente_role['_id']

                    # Obtener la colección de usuarios
                    users_collection = self.db.get_collection('users')

                    hashed_password = generate_password_hash(password)

                    # Insertar el usuario en la colección "users" con referencia al paciente correspondiente
                    user_id = users_collection.insert_one({
                        'email': email,
                        'password': hashed_password,
                        'paciente_id': paciente_id,
                        'role_id': paciente_role_id
                    }).inserted_id

                    if user_id:
                        # self.show_dialog("Bienvenido", f"Bienvenido, {p_nombre}.")
                        screen_manager.current = "login"
                    else:
                        self.show_dialog("Error", "Error al registrar.")
                else:
                    self.show_dialog(
                        "Error", "Error al registrar el paciente.")
            except Exception as e:
                print(f"Error al registrar: {str(e)}")
                self.show_dialog("Error", "Error al registrar.")'''

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
            self.previous_text = text
            mensaje_nombre.opacity = 0
            return text
        else:
            mensaje_nombre.opacity = 1
            return self.previous_text

    def on_textinput(self, instance, text, mensaje_nombre):
        instance.text = self.solo_letras(instance.text, mensaje_nombre)

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
