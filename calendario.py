'''
    def on_save(self, instance, value, date_range):
        
        
        Eventos a los que se llama cuando se hace clic en el botón del cuadro de diálogo "Aceptar".

        :type instance: <kivymd.uix.picker.MDDatePicker object>;
        :param value: Fecha;
        :type value: <class 'datetime.date'>;
        :param date_range: lista de 'datetime.date' objetos del rango seleccionado;
        :type date_range: <class 'list'>;
        
        date_text = value.strftime('%Y-%m-%d')  # Convierte la fecha en formato de texto
        self.ids.f_nacimiento.text = date_text  # Actualiza el texto del campo de entrada
        print(instance, value, date_range)


    def on_cancel(self, instance, value):
        Eventos a los que se llama cuando se hace clic en el botón del cuadro de diálogo "CANCELAR".

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

'''
