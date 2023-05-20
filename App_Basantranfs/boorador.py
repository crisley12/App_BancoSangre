from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.core.window import Window

Window.size = (350,500)

kV = '''
MDScreen:

    FitImage:
        source: 'App_Basantranfs\img\login.png'
        

    BoxLayout: 
        size_hint: None, None
        size: 400, 600
        elevation: 10
        padding: 10
        spacing: 15
        orientation: 'vertical'
        
        MDLabel:
            text: "Basantranfs"
            pos_hint: {"center_x": .5, "center_y": .20}
            halign: 'center'
            font_size: '40sp'
            theme_text_color: 'Custom'
            text_color: 255/255, 255/255, 255/255, 1

    
        MDTextFieldRound:
            id: email
            icon_left: 'email'
            hint_text: "Ingrese el correo"
            color_active: [1, 1, 1, 1]
            foreground_color: 0, 0, 0
            size_hint_x: None
            width: 220
            font_size: 20
            pos_hint: {"center_x": 0.5}
        
        MDTextFieldRound:
            id: password
            icon_left: 'lock'
            hint_text: "Ingrese la contraseña"
            color_active: [1, 1, 1, 1]
            foreground_color: 0, 0, 0
            size_hint_x: None
            width: 220
            font_size: 20
            pos_hint: {"center_x": 0.5}
            password: True


        MDFillRoundFlatButton:
            text: "Iniciar Session"
            color_active: [1, 1, 1, 1]
            foreground_color: 0, 0, 0
            font_size: 15
            pos_hint: {"center_x": 0.5} 
            opacity: 1  
            on_press: app.login()
'''



class MainApp(MDApp):
     dialog = None  
     

#Colores de la pantala 
     def build(self) : 
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Gray'
        self.theme_cls.accent_palette = 'Blue'

        return Builder.load_string(kV)

#Login configuracion

     def login(self):
        if self.root.ids.email.text == 'c' and self.root.ids.password.text == '123':
         if not self.dialog:
            self.dialog = MDDialog(
             title = 'Login',
             text = f"Bienvenido {self.root.ids.email.text}!",
             buttons = [
                MDFlatButton(
                text = "ok", text_color = self.theme_cls.accent_color,
                on_release = self.close 
                ),
             ], 
          )         
            self.dialog.open()
         
     def close(self):
        self.dialog.dismiss()

MainApp().run()


