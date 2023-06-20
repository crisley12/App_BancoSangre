from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField

KV = """
MDFloatLayout:
    size_hint: .35, .05
    pos_hint: {"center_x": .3, "center_y": .80}
    canvas:
        Color:
            rgb: (238/255, 238/255, 1)
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [25]
    TextInput:
        id: cedula
        input_filter: 'int'
        on_text: self.text = app.solo_numeros(self.text, root.ids.mensaje_numero)
        #font_name: "Poppins"
        hint_text: "Cédula"
        size_hint: 1, None
        pos_hint: {"center_x": .5, "center_y": .5}
        height: self.minimum_height
        multiline: False
        cursor_color: 0, 0, 0
        cursor_width: '2sp'
        foreground_color: 0, 0, 0
        background_color: 0, 0, 0, 0
        padding: [10]
        font_size: '13sp'
        on_text: root.check_length_cedula()
        on_focus:
            if self.focus: self.text = "V-" + self.text.lstrip("V-")
"""

class MyApp(MDApp):
    def build(self):
        Window.size = (300, 200)
        return Builder.load_string(KV)

    def solo_numeros(self, text, label):
        if text:
            return "".join([c for c in text if c.isdigit()])
        return ""

    def check_length_cedula(self):
        cedula = self.root.ids.cedula.text
        if len(cedula) > 1 and not cedula.startswith("V-"):
            self.root.ids.cedula.text = "V-" + cedula

if __name__ == '__main__':
    MyApp().run()
