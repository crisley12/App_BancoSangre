from kivymd.uix.screen import MDScreen
from kivy.lang import Builder


class DonateScreen(MDScreen):
    def __init__(self, **kwargs) -> None:
        Builder.load_file('screen_Kv/donate_screen.kv')
        super(DonateScreen, self).__init__(**kwargs)
        self.respuestas = {}  # Diccionario para almacenar las respuestas


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
        # pregunta_actual = self.ids.carusel.current_slide.name  # Obtener el nombre de la pregunta actual
        # respuesta = self.get_selected_answer(pregunta_actual)  # Obtener la respuesta seleccionada
        # if respuesta is not None:
        # self.respuestas[pregunta_actual] = respuesta  # Guardar la respuesta en el diccionario

        #  Cambio de color e icono a la barra de progreso
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
        # pregunta_actual = self.ids.carusel.current_slide.name
        # respuesta = self.get_selected_answer(pregunta_actual)
        # if respuesta is not None:
        # self.respuestas[pregunta_actual] = respuesta

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
        # pregunta_actual = self.ids.carusel.current_slide.name
        # respuesta = self.get_selected_answer(pregunta_actual)
        # if respuesta is not None:
        # self.respuestas[pregunta_actual] = respuesta

        self.next_donate = self.ids.carusel.load_next(mode="next")
        self.ids.label4.text_color = [1, 0, 0, 1]
        self.ids.progress4.value = 100
        self.ids.progress4.bar_color = [1, 0, 0, 1]
        self.icon_donate = self.ids.icon4.text_color = [1, 0, 0, 1]
        self.ids.icon4.icon = "check-circle"

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
        # pregunta_actual = self.ids.carusel.current_slide.name
        # respuesta = self.get_selected_answer(pregunta_actual)
        # if respuesta is not None:
        # self.respuestas[pregunta_actual] = respuesta

        self.next_donate = self.ids.carusel.load_next(mode="next")
        self.ids.label5.text_color = [1, 0, 0, 1]
        self.ids.progress5.value = 100
        self.ids.progress5.bar_color = [1, 0, 0, 1]
        self.icon_donate = self.ids.icon5.text_color = [1, 0, 0, 1]
        self.ids.icon5.icon = "check-circle"

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
        # pregunta_actual = self.ids.carusel.current_slide.name
        # respuesta = self.get_selected_answer(pregunta_actual)
        # if respuesta is not None:
        # self.respuestas[pregunta_actual] = respuesta

        self.next_donate = self.ids.carusel.load_next(mode="next")
        self.ids.label6.text_color = [1, 0, 0, 1]
        self.ids.progress6.value = 100
        self.ids.progress6.bar_color = [1, 0, 0, 1]
        self.icon_donate = self.ids.icon6.text_color = [1, 0, 0, 1]
        self.ids.icon6.icon = "check-circle"

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
        # pregunta_actual = self.ids.carusel.current_slide.name
        # respuesta = self.get_selected_answer(pregunta_actual)
        # if respuesta is not None:
        # self.respuestas[pregunta_actual] = respuesta

        self.next_donate = self.ids.carusel.load_next(mode="next")
        self.ids.label7.text_color = [1, 0, 0, 1]
        self.ids.progress7.value = 100
        self.ids.progress7.bar_color = [1, 0, 0, 1]
        self.icon_donate = self.ids.icon7.text_color = [1, 0, 0, 1]
        self.ids.icon7.icon = "check-circle"

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
        # pregunta_actual = self.ids.carusel.current_slide.name
        # respuesta = self.get_selected_answer(pregunta_actual)
        # if respuesta is not None:
        # self.respuestas[pregunta_actual] = respuesta

        self.next_donate = self.ids.carusel.load_next(mode="next")
        self.ids.label8.text_color = [1, 0, 0, 1]
        self.ids.progress8.value = 100
        self.ids.progress8.bar_color = [1, 0, 0, 1]
        self.icon_donate = self.ids.icon8.text_color = [1, 0, 0, 1]
        self.ids.icon8.icon = "check-circle"

    def previous8(self):
        self.previous_donate = self.ids.carusel.load_previous()
        self.ids.label8.text_color = [0, 0, 0, 1]
        self.ids.icon8.text_color = [0, 0, 0, 1]
        self.ids.progress8.value = 0
        self.ids.icon8.icon = "numeric-8-circle"


######################################################
#           NOVENA PANTALLA
#######################################################
'''
    def next9(self):
        pregunta_actual = self.ids.carusel.current_slide.name 
        respuesta = self.get_selected_answer(pregunta_actual) 
        if respuesta is not None:
            self.respuestas[pregunta_actual] = respuesta   

        self.next_donate = self.ids.carusel.load_next(mode="")
        self.ids.label9.text_color = [1, 0, 0, 1]
        self.icon_donate = self.ids.icon9.text_color = [1, 0, 0, 1]
        self.ids.icon9.icon = "check-circle"


    def previous9(self):
        self.previous_donate = self.ids.carusel.load_previous()
        self.ids.label9.text_color = [0, 0, 0, 1]
        self.ids.icon9.text_color = [0, 0, 0, 1]
        self.ids.progress9.value = 0
        self.ids.icon9.icon = "numeric-9-circle"



#Obtener la respuesta seleccionada según la pregunta actual
    def get_selected_answer(self, pregunta):
            if pregunta == 'pantalla2':
                if self.ids.less_than_50kg.state == 'down':
                    return 'menos de 50kg'
                elif self.ids.from_50kg.state == 'down':
                    return 'a partir de 50kg'
                elif self.ids.from_50kg_to_65kg.state == 'down':
                    return '50kg a 65kg'
                elif self.ids.from_65kg_to_80kg.state == 'down':
                    return '65kg a 80kg'
                elif self.ids.more_than_80kg.state == 'down':
                    return '+ de 80kg'
            elif pregunta == 'pantalla3':
                if self.ids.vaccinated_yes.state == 'down':
                    return 'Si'
                elif self.ids.vaccinated_no.state == 'down':
                    return 'No'


# Realizar las validaciones y tomar decisiones según las respuestas almacenadas en self.respuestas

def verificar_apto_para_donar(self):
        peso = self.respuestas.get('label2', '')
        vacunado = self.respuestas.get('label3', '')

        if peso == 'menos de 50kg' and vacunado == 'Si':
            # No apto para donar
            print("No eres apto para donar sangre.")
        else:
            # Apto para donar
            print("Eres apto para donar sangre.")

'''


'''
    def update_progress(self):
        pregunta_actual = self.ids.carusel.current_slide.name  # Obtener el nombre de la pregunta actual
        progreso = int(pregunta_actual[-1]) * 25  # Calcular el progreso actual (25%, 50%, 75%, 100%)
        self.ids.progress1.value = progreso
'''


'''
 MDTextField:
                            hint_text: "Firste Name"
                            size_hint_x: .8
                            pos_hint: {"center_x": .5, "center_y": .48}
                        MDTextField:
                            hint_text: "Last Name"
                            size_hint_x: .8
                            pos_hint: {"center_x": .5, "center_y": .36}
'''
