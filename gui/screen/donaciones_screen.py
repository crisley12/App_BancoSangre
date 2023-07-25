from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
import requests


class DonacionesScreen(MDScreen):
    def __init__(self, **kwargs) -> None:
          Builder.load_file('screen_Kv/donaciones_screen.kv')
          super().__init__(**kwargs)
    #       self.obtener_donaciones_paciente()  

    # def obtener_donaciones_paciente(self):
    #     url_donaciones = 'http://localhost:5000/obtener_donaciones_paciente'
    #     response = requests.get(url_donaciones)
    #     print(response)
    #     if response.status_code == 200:
    #         donaciones = response.json()
    #         donacion_data = []
    #         for i, item in enumerate(donaciones, start=1):
    #             if isinstance(item, dict):
    #                 row = (
    #                     f"{i}",
    #                     item['localidad'],
    #                     item['numero_bolsa'],
    #                     item['hemoglobina'],
    #                     item['volumen'],
    #                     item['fecha_hora'],
    #                     item['paciente_id'],
    #                 )
    #                 donacion_data.append(row)

    #         self.data_table = MDDataTable(
    #             pos_hint={'center_y': 0.3, 'center_x': 0.5},
    #             size_hint=(0.9, 0.5),
    #             use_pagination=True,
    #             elevation=1,
    #             background_color_header="#F41F05",
    #             check=True,
    #             column_data=[
    #                 ("No.", dp(30)),
    #                 ("Localidad", dp(50)),
    #                 ("Número de Bolsa", dp(30)),
    #                 ("Hemoglobina", dp(30)),
    #                 ("Volumen", dp(30)),
    #                 ("Fecha y Hora", dp(50)),
    #                 ("ID Paciente", dp(50)),
    #             ],
    #             row_data=donacion_data,
    #         )
    #         self.data_table.bind(on_row_press=self.on_row_press)
    #         self.data_table.bind(on_check_press=self.on_check_press)
    #         self.ids.donaciones.add_widget(self.data_table)
    #         self.checkcomprobar = 5
    #     else:
    #         print("Error al obtener las donaciones")

    
        
