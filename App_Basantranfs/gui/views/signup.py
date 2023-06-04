from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from kivymd.uix.list import OneLineListItem
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
#from kivymd.theming import ThemeManager


class Signup(MDScreen):
    db = None

    def __init__(self, **kwargs) -> None:
        Builder.load_file("kv/signup.kv")
        super(Signup, self).__init__(**kwargs)
        self.database = kwargs.get('database')
        self.t_sangre = self.ids.t_sangre
        self.t_sexo = self.ids.t_sexo
        self.create_dropdown()
        self.validacionRegistro()
    

#################################################
#            SELECTOR DE FECHA
#################################################

    def on_save(self, instance, value, date_range):
        
        '''
        Eventos a los que se llama cuando se hace clic en el botón del cuadro de diálogo "Aceptar".

        :type instance: <kivymd.uix.picker.MDDatePicker object>;
        :param value: Fecha;
        :type value: <class 'datetime.date'>;
        :param date_range: lista de 'datetime.date' objetos del rango seleccionado;
        :type date_range: <class 'list'>;
        '''
        date_text = value.strftime('%Y-%m-%d')  # Convierte la fecha en formato de texto
        self.ids.f_nacimiento.text = date_text  # Actualiza el texto del campo de entrada
        print(instance, value, date_range)


    def on_cancel(self, instance, value):
        '''Eventos a los que se llama cuando se hace clic en el botón del cuadro de diálogo "CANCELAR".'''

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



#################################################
#            LISTA DESPLEGABLE
#################################################

    def create_dropdown(self):
        self.dropdown_1 = DropDown()
        self.dropdown_2 = DropDown()
      

        items_1 = ['AB+', 'AB-', 'O+', 'O-', 'B+', 'B-', 'A+', 'A-']
        for item_text in items_1:
            item = OneLineListItem(text=item_text)
            item.bind(on_release=self.menu_callback_1)
            self.dropdown_1.add_widget(item) 

        
        items_2 = ['F', 'M']
        for item_text in items_2:
            item = OneLineListItem(text=item_text)
            item.bind(on_release=self.menu_callback_2)
            self.dropdown_2.add_widget(item)

    def menu_callback_1(self, instance) -> None:
        selected_text = instance.text
        print(selected_text)
        self.t_sangre.text = selected_text
        self.dropdown_1.dismiss()

    def menu_callback_2(self, instance) -> None:
        selected_text = instance.text
        print(selected_text)
        self.t_sexo.text = selected_text
        self.dropdown_2.dismiss()


#################################################
#            INPUT CEDULA 
#################################################

    Max_c = 8

    def check_length_cedula(self):
        cedula = self.ids.cedula
        text = cedula.text
        if len(text) > self.Max_c:
            cedula.foreground_color = 1, 0, 0, 1  # Cambiar a color rojo
        else:
            cedula.foreground_color = 0, 0, 0, 1  # Restaurar el color original

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

####################################################
#                VALIDACION 
####################################################

    def validacionRegistro(self):
      # Obtener el texto de los campos de usuario y contraseña
      cedula = self.ids.cedula.text
      p_apellido = self.ids.p_apellido.text
      s_apellido  = self.ids.s_apellido.text
      p_nombre  = self.ids.p_nombre.text
      s_nombre  = self.ids.s_nombre.text
      n_telefono  = self.ids.n_telefono.text
      t_sangre  = self.ids.t_sangre.text
      t_sexo  = self.ids.t_sexo.text
      f_nacimiento  = self.ids.f_nacimiento.text
      email  = self.ids.email.text
      password  = self.ids.password.text
        
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
    
      # Obtener la colección de usuarios
      users_collection = self.db.get_collection('users')

      # Buscar al usuario en la base de datos
      registro = users_collection.insert_one({'cedula': cedula, 'p_apellido': p_apellido, 's_apellido': s_apellido, 'p_nombre': p_nombre, 's_nombre': s_nombre,
                                          'n_telefono': n_telefono, 't_sangre': t_sangre, 't_sexo': t_sexo,'f_nacimiento': f_nacimiento, 'email': email, 'password': password})

      if registro is None:
          self.show_dialog("Error", "error al registrar.")
      else:
        self.show_dialog("Bienvenido", f"Bienvenido, {p_nombre}.")
        self.current = "login"
        
            
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
