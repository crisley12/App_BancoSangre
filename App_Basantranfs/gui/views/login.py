from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton




class Login(MDScreen):
    db = None

    def __init__(self, **kwargs) -> None:
      Builder.load_file("kv/login.kv")
      super().__init__(**kwargs)
      self.database = kwargs.get('database')
      self.validacionUser()


####################################################
#                VALIDACION 
####################################################

    def validacionUser(self):
      # Obtener el texto de los campos de usuario y contraseña
      username = self.ids.email.text
      password = self.ids.password.text
        
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
  
        
    
