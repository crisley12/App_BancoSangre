from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
import requests
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen


class DonateScreen(MDScreen):
    
    #guardar_respuestas = ObjectProperty(None)
    paciente_id = ObjectProperty(None)  # Esta variable almacenará el ID del paciente logueado
    paciente_nombre = ObjectProperty(None)  # Esta variable almacenará el nombre del paciente logueado

    respuesta = {}  # Variable global para almacenar las respuestas
    
    def __init__(self, **kwargs) -> None:
        Builder.load_file('screen_Kv/donate_screen.kv')
        super(DonateScreen, self).__init__(**kwargs)
        
        self.respuesta = {}

    def show_dialog(self, title, message):
        dialog = MDDialog(
            title=title,
            text=message,
        )
        dialog.open()


######################################################
#           PRIMERA PANTALLA
#######################################################

    def next(self):
        self.next_donate = self.ids.carusel.load_next(mode="next")
        self.ids.label1.text_color = [1, 0, 0, 1]
        self.ids.progress1.value = 100
        self.ids.progress1.bar_color = [1, 0, 0, 1]
        self.icon_donate = self.ids.icon1.text_color = [1, 0, 0, 1]
        self.ids.icon1.icon = "check-circle"

    def previous1(self):
        self.previous_donate = self.ids.carusel.load_previous()
        self.ids.label1.text_color = [0, 0, 0, 1]
        self.ids.icon1.text_color = [0, 0, 0, 1]
        self.ids.progress1.value = 0
        self.ids.icon1.icon = "numeric-1-circle"


######################################################
#           SEGUNDA PANTALLA
#######################################################

    def next2(self):
        pregunta = "En los últimos 30 días has sido vacunado contra"
        respuestas = {}

        # Verificar si el botón "no_vacunado" está seleccionado
        if self.ids.no_vacunado.state == "down":
            respuesta_no_vacunado = self.ids.no_vacunado.text
            respuestas[pregunta] = respuesta_no_vacunado
        else:
            self.show_dialog(
                "No apto para donar", "No puede estar vacunado contra esas enfermedades. LEA LOS REQUISITOS!")
            return
        
        # Guardar respuestas en el diccionario global
        self.respuesta.update(respuestas)
        print(respuestas)
        
        # Continuar con la siguiente pantalla
        self.next_donate = self.ids.carusel.load_next(mode="next")
        self.ids.label2.text_color = [1, 0, 0, 1]
        self.ids.progress2.value = 100
        self.ids.progress2.bar_color = [1, 0, 0, 1]
        self.icon_donate = self.ids.icon2.text_color = [1, 0, 0, 1]
        self.ids.icon2.icon = "check-circle"


#  Cambia devuelta al color inicial


    def previous2(self):

        self.previous_donate = self.ids.carusel.load_previous()
        self.ids.label2.text_color = [0, 0, 0, 1]
        self.ids.icon2.text_color = [0, 0, 0, 1]
        self.ids.progress2.value = 0
        self.ids.icon2.icon = "numeric-2-circle"

######################################################
#           TERCERA PANTALLA
#######################################################

    def next3(self):
        pregunta = "Tomaste algunos de los siguientes medicamento en los últimos 7 días"
        respuestas = {}

        if self.ids.no_medicamentos.state == "down":
            respuesta_no_medicamentos = self.ids.no_medicamentos.text
            respuestas[pregunta] = respuesta_no_medicamentos
        else:
            self.show_dialog(
                "No apto para donar", "No puede tomar medicamentos contra enfermedades días antes. LEA LOS REQUISITOS!")
            return

        self.respuesta.update(respuestas)
        print(respuestas)

        self.next_donate = self.ids.carusel.load_next(mode="next")
        self.ids.label3.text_color = [1, 0, 0, 1]
        self.ids.progress3.value = 100
        self.ids.progress3.bar_color = [1, 0, 0, 1]
        self.icon_donate = self.ids.icon3.text_color = [1, 0, 0, 1]
        self.ids.icon3.icon = "check-circle"
        print(self.respuesta)

        self.next_donate = self.ids.carusel.load_next(mode="next")
        self.ids.label3.text_color = [1, 0, 0, 1]
        self.ids.progress3.value = 100
        self.ids.progress3.bar_color = [1, 0, 0, 1]
        self.icon_donate = self.ids.icon3.text_color = [1, 0, 0, 1]
        self.ids.icon3.icon = "check-circle"

    def previous3(self):
        self.previous_donate = self.ids.carusel.load_previous()
        self.ids.label3.text_color = [0, 0, 0, 1]
        self.ids.icon3.text_color = [0, 0, 0, 1]
        self.ids.progress3.value = 0
        self.ids.icon3.icon = "numeric-3-circle"

######################################################
#           CUARTAPANTALLA
#######################################################

    def next4(self):

        pregunta = "Padeces de alguna infección o enfermedad actualmente"
        respuestas = {}

        if self.ids.no_infeccion.state == "down":
            respuesta_no_infeccion = self.ids.no_infeccion.text
            respuestas[pregunta] = respuesta_no_infeccion
        else:
            self.show_dialog(
                "No apto para donar", "No puede tener alguna infección u enfermedad grave para donar. LEA LOS REQUISITOS!")
            return

        self.respuesta.update(respuestas)
        print(respuestas)

        self.next_donate = self.ids.carusel.load_next(mode="next")
        self.ids.label4.text_color = [1, 0, 0, 1]
        self.ids.progress4.value = 100
        self.ids.progress4.bar_color = [1, 0, 0, 1]
        self.icon_donate = self.ids.icon4.text_color = [1, 0, 0, 1]
        self.ids.icon4.icon = "check-circle"
        print(self.respuesta)

    def previous4(self):
        self.previous_donate = self.ids.carusel.load_previous()
        self.ids.label4.text_color = [0, 0, 0, 1]
        self.ids.icon4.text_color = [0, 0, 0, 1]
        self.ids.progress4.value = 0
        self.ids.icon4.icon = "numeric-4-circle"


######################################################
#           QUINTA PANTALLA
#######################################################


    def next5(self):
        pregunta = "Has padecido alguna de las siguientes enfermedades graves"
        respuestas = {}

        if self.ids.no_enfermedades.state == "down":
            respuesta_no_enfermedades = self.ids.no_enfermedades.text
            respuestas[pregunta] = respuesta_no_enfermedades
        else:
            self.show_dialog(
                "No apto para donar", "No puedes tener o haber tenido esas enfermades. LEA LOS REQUISITOS!")
            return

        self.respuesta.update(respuestas)
        print(respuestas)

        self.next_donate = self.ids.carusel.load_next(mode="next")
        self.ids.label5.text_color = [1, 0, 0, 1]
        self.ids.progress5.value = 100
        self.ids.progress5.bar_color = [1, 0, 0, 1]
        self.icon_donate = self.ids.icon5.text_color = [1, 0, 0, 1]
        self.ids.icon5.icon = "check-circle"
        print(self.respuesta)

    def previous5(self):
        self.previous_donate = self.ids.carusel.load_previous()
        self.ids.label5.text_color = [0, 0, 0, 1]
        self.ids.icon5.text_color = [0, 0, 0, 1]
        self.ids.progress5.value = 0
        self.ids.icon5.icon = "numeric-5-circle"


######################################################
#           SEXTA PANTALLA
#######################################################


    def next6(self):
        pregunta = "Consumiste alguna bebida alcoholica en los últimos 3 días"
        respuestas = {}

        if self.ids.no_beber.state == "down":
            respuesta_no_beber = self.ids.no_beber.text
            respuestas[pregunta] = respuesta_no_beber
        else:
            self.show_dialog(
                "No apto para donar", "No beber ni fumar antes de donar por lo menos el intervalo debe ser de 24 hrs. LEA LOS REQUISITOS!")
            return

        self.respuesta.update(respuestas)
        print(respuestas)

        self.next_donate = self.ids.carusel.load_next(mode="next")
        self.ids.label6.text_color = [1, 0, 0, 1]
        self.ids.progress6.value = 100
        self.ids.progress6.bar_color = [1, 0, 0, 1]
        self.icon_donate = self.ids.icon6.text_color = [1, 0, 0, 1]
        self.ids.icon6.icon = "check-circle"
        print(self.respuesta)

    def previous6(self):
        self.previous_donate = self.ids.carusel.load_previous()
        self.ids.label6.text_color = [0, 0, 0, 1]
        self.ids.icon6.text_color = [0, 0, 0, 1]
        self.ids.progress6.value = 0
        self.ids.icon6.icon = "numeric-6-circle"


######################################################
#           SEPTIMA PANTALLA
#######################################################

    def next7(self):
        pregunta = "Posees tatuajes o perforaciones hechos recientemente"
        respuestas = {}

        if self.ids.tatoo_mas.state == "down":
            respuesta_tatoo_mas = self.ids.tatoo_mas.text
            respuestas[pregunta] = respuesta_tatoo_mas

        if self.ids.no_tatoo.state == "down":
            respuesta_no_tatoo = self.ids.no_tatoo.text
            respuestas[pregunta] = respuesta_no_tatoo

        if not respuestas:
            self.show_dialog(
                "No apto para donar", "Por lo menos tienes que esperar un año despues de realizarte el tatuaje o perforación para poder donar. LEA LOS REQUISITOS!")
            return

        self.respuesta.update(respuestas)
        print(respuestas)
        self.next_donate = self.ids.carusel.load_next(mode="next")
        self.ids.label7.text_color = [1, 0, 0, 1]
        self.ids.progress7.value = 100
        self.ids.progress7.bar_color = [1, 0, 0, 1]
        self.icon_donate = self.ids.icon7.text_color = [1, 0, 0, 1]
        self.ids.icon7.icon = "check-circle"
        print(self.respuesta)

    def previous7(self):
        self.previous_donate = self.ids.carusel.load_previous()
        self.ids.label7.text_color = [0, 0, 0, 1]
        self.ids.icon7.text_color = [0, 0, 0, 1]
        self.ids.progress7.value = 0
        self.ids.icon7.icon = "numeric-7-circle"


######################################################
#           OCTAVA PANTALLA
#######################################################

    def next8(self):
        pregunta = "Has donado anteriormente"
        respuestas = {}

        if self.ids.donacion_mas.state == "down":
            respuesta_donacion_mas = self.ids.donacion_mas.text
            respuestas[pregunta] = respuesta_donacion_mas

        if self.ids.donacion_no.state == "down":
            respuesta_donacion_no = self.ids.donacion_no.text
            respuestas[pregunta] = respuesta_donacion_no

        if not respuestas:
            self.show_dialog(
                "No apto para donar", "Por lo menos tienes que esperar un año despues de realizarte el tatuaje o perforación para poder donar. LEA LOS REQUISITOS!")
            return

        self.respuesta.update(respuestas)
        print(respuestas)
        self.next_donate = self.ids.carusel.load_next(mode="next")
        self.ids.label8.text_color = [1, 0, 0, 1]
        self.ids.progress8.value = 100
        self.ids.progress8.bar_color = [1, 0, 0, 1]
        self.icon_donate = self.ids.icon8.text_color = [1, 0, 0, 1]
        self.ids.icon8.icon = "check-circle"

    def previous8(self):
        self.ids.label8.text_color = [0, 0, 0, 1]
        self.ids.icon8.text_color = [0, 0, 0, 1]
        self.ids.progress8.value = 0
        self.ids.icon8.icon = "numeric-8-circle"
        self.ids.label7.text_color = [0, 0, 0, 1]
        self.ids.icon7.text_color = [0, 0, 0, 1]
        self.ids.progress7.value = 0
        self.ids.icon7.icon = "numeric-7-circle"
        self.ids.label6.text_color = [0, 0, 0, 1]
        self.ids.icon6.text_color = [0, 0, 0, 1]
        self.ids.progress6.value = 0
        self.ids.icon6.icon = "numeric-6-circle"
        self.ids.label5.text_color = [0, 0, 0, 1]
        self.ids.icon5.text_color = [0, 0, 0, 1]
        self.ids.progress5.value = 0
        self.ids.icon5.icon = "numeric-5-circle"
        self.ids.label4.text_color = [0, 0, 0, 1]
        self.ids.icon4.text_color = [0, 0, 0, 1]
        self.ids.progress4.value = 0
        self.ids.icon4.icon = "numeric-4-circle"
        self.ids.label3.text_color = [0, 0, 0, 1]
        self.ids.icon3.text_color = [0, 0, 0, 1]
        self.ids.progress3.value = 0
        self.ids.icon3.icon = "numeric-3-circle"
        self.ids.label2.text_color = [0, 0, 0, 1]
        self.ids.icon2.text_color = [0, 0, 0, 1]
        self.ids.progress2.value = 0
        self.ids.icon2.icon = "numeric-2-circle"
        self.ids.label1.text_color = [0, 0, 0, 1]
        self.ids.icon1.text_color = [0, 0, 0, 1]
        self.ids.progress1.value = 0
        self.ids.icon1.icon = "numeric-1-circle"
        # Reiniciar el diccionario de respuestas
        self.respuestas = {}
        self.ids.carusel.index = 0


######################################################
#           NOVENA PANTALLA
#######################################################

    def next9(self):
        pregunta = "Has finalizado el cuestionario. ¿Deseas guardar tus respuestas?"
        respuestas = {}

        if self.ids.guardar_respuestas.state == "down":
            respuesta_guardar = self.ids.guardar_respuestas.text
            respuestas[pregunta] = respuesta_guardar
        else:
            return self.show_dialog("Información no guardada",
                            "Tus respuestas no serán guardadas en la base de datos.")

        # Verificar que se tiene la información del paciente logueado
        if not self.paciente_id or not self.paciente_nombre:
            self.show_dialog("Error", "No se ha encontrado la información del paciente logueado.")
            return
        
         # Asignar las respuestas a la variable respuesta
        self.respuesta = respuestas
        
        # Guardar respuestas en la base de datos
        url = 'http://localhost:5000/guardar_respuestas'
        data ={
            "paciente_id": self.paciente_id,
            "paciente_nombre": self.paciente_nombre,
            "respuestas": self.respuesta
        }
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            print('Respuestas guardadas exitosamente.')
            return self.show_dialog("Registro exitoso", "Exitoso")
        else:
            print('Error al guardar las respuestas:', response.json())

         #Continuar con la siguiente pantalla
        self.next_donate = self.ids.carusel.load_next(mode="")

        self.ids.label9.text_color = [1, 0, 0, 1]
        self.ids.progress9.value = 100
        self.ids.progress9.bar_color = [1, 0, 0, 1]
        self.icon_donate = self.ids.icon9.text_color = [1, 0, 0, 1]
        self.ids.icon9.icon = "check-circle"

