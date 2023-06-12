from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from views.login_views import Login
from views.signup_views import Signup
from conection import Database
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import re
from werkzeug.security import generate_password_hash, check_password_hash

from kivy.lang import Builder
Window.size = (350, 600)


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database(database_name='banco_de_sangre')

# Constructor de la interfaz

    def build(self) -> None:
        global screen_manager
        screen_manager = ScreenManager()
        # self.manager = ScreenManager(transition = NoTransition())
        screen_manager.add_widget(Builder.load_file("kv/main.kv"))
        screen_manager.add_widget(Login(name='login'))
        screen_manager.add_widget(Signup(name='signup'))
        return screen_manager


# Transicion de pantalla de inicio a --> LoginScreen

    def on_start(self) -> None:
        Clock.schedule_once(self.login, 3)

    def login(self, *args) -> None:
        screen_manager.current = "login"
        
    
    def validacionUser(self):
        # Obtener el texto de los campos de usuario y contraseña
        login_screen = screen_manager.get_screen('login')
        username = login_screen.ids.email.text
        password = login_screen.ids.password.text
            
        # Verificar si los campos están vacíos
        if not username or not password:
            self.show_dialog("Error", "Por favor, complete todos los campos.")
            return
        
        # Obtener la colección de usuarios
        users_collection = self.db.get_collection('users')

        # Buscar al usuario en la base de datos
        user = users_collection.find_one({'email': username, 'password': password})

        # Verificar si el usuario fue encontrado o no
        if user is None:
            self.show_dialog("Error", "Usuario o contraseña incorrecto.")
        else:
            self.show_dialog("Bienvenido", f"Bienvenido, {user['p_nombre']}.")
            
# Validar el formato del email
    def validar_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None
    
#Validar Solo numeros
    def solo_numeros(self, text, mensaje_numero):
        if text.isdigit():
            mensaje_numero.opacity = 0
            return text
        else:
            mensaje_numero.opacity = 1
            return ""

#Valida solo Letras
    def solo_letras(self, text, mensaje_nombre):
        if text.isalpha():
            mensaje_nombre.opacity = 0
            return text
        else:
            mensaje_nombre.opacity = 1
            return ""

              
    def validacionRegistro(self):
        # Obtener el texto de los campos de usuario y contraseña
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
            self.show_dialog("Error", "Por favor, ingrese un correo electrónico válido.")
            return

        # Verificar si los campos están vacíos
        campo_vacio = []
        if not cedula:
            campo_vacio.append("cedula")
        if not p_apellido:
            campo_vacio.append("p_apellido")
        if not s_apellido:
            campo_vacio.append("s_apellido")
        if not p_nombre:
            campo_vacio.append("p_nombre")
        if not s_nombre:
            campo_vacio.append("s_nombre")
        if not n_telefono:
            campo_vacio.append("n_telefono")
        if not t_sangre:
            campo_vacio.append("t_sangre")
        if not t_sexo:
            campo_vacio.append("t_sexo")
        if not f_nacimiento:
            campo_vacio.append("f_nacimiento")
        if not email:
            campo_vacio.append("email")
        if not password:
            campo_vacio.append("password")

        if campo_vacio:
            campos_str = ", ".join(campo_vacio)
            mensaje = f"Por favor, complete los siguientes campos: {campos_str}"
            self.show_dialog("Error", mensaje)
            return

        # Obtener la colección de pacientes
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
                    paciente_role = roles_collection.find_one({'nombre': 'paciente'})

                    if not paciente_role:
                        # Si el rol "paciente" no existe, se crea
                        paciente_role_id = roles_collection.insert_one({'nombre': 'paciente'}).inserted_id
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
                        #self.show_dialog("Bienvenido", f"Bienvenido, {p_nombre}.")
                        screen_manager.current = "login"
                    else:
                        self.show_dialog("Error", "Error al registrar.")
                else:
                    self.show_dialog("Error", "Error al registrar el paciente.")
            except Exception as e:
                print(f"Error al registrar: {str(e)}")
                self.show_dialog("Error", "Error al registrar.")



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
            
if __name__ == '__main__':
    MainApp().run()
