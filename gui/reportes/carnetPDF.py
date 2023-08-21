from fpdf import FPDF
from datetime import datetime
from pymongo import MongoClient

# Realizar la conexión a la base de datos
client = MongoClient('localhost', 27017)
database = client['banco_de_sangre']
pacientes_collection = database['pacientes']
pacientes = pacientes_collection.find()


# Convertir las dimensiones de mm a puntos (1 mm = 2.83465 puntos)
tarjeta_ancho_pts = 85.60
tarjeta_alto_pts = 53.98



# Clase PDF que hereda de FPDF
class TarjetaPDF(FPDF):
    
    
    def header(self):
         # Obtener los datos del paciente desde la base de datos
        paciente = pacientes_collection.find_one()  # Suponiendo que solo obtienes un paciente

        # Obtener los valores de las variables del paciente desde MongoDB
        nombre_completo = f"{paciente['p_nombre']} {paciente['s_nombre']} {paciente['p_apellido']} {paciente['s_apellido']}"
        tipo_sangre = paciente['t_sangre']
        fecha_nacimiento = paciente['f_nacimiento']

        self.set_line_width(0.3)  # Grosor del borde
        self.set_draw_color(0, 0, 0)  # Color del borde (negro)
        self.rect(10, 10, tarjeta_ancho_pts, tarjeta_alto_pts)  # Dibujar rectángulo
        self.image('gui/reportes/img/Logo.jpg', x=14, y=45, w=45)
        self.set_xy(15, 20)
        self.set_font('Arial', 'B', 8)
        self.set_text_color(189, 13, 19)
        self.cell(28, 5, 'Nombre y Apellido:', 0, 0, 'L', 0)
        self.set_font('Arial', '', 8)
        self.set_text_color(40,40,40)
        self.cell(48, 5, nombre_completo, 0, 0, 'L', 0)
        self.set_xy(17, 27)
        self.set_draw_color(189, 13, 19)
        self.set_line_width(0.2) 
        self.multi_cell(12, 5, f'Grupo: {tipo_sangre}', 1, 'C', 0)
        self.set_xy(30, 27)
        self.multi_cell(17, 5, f'Factor RH: {tipo_sangre}', 1, 'C', 0)
        self.set_xy(60, 27)
        self.multi_cell(30, 5, f'Fecha de nacimiento: {fecha_nacimiento}', 1, 'C', 0)
        self.set_xy(60, 53)
        self.multi_cell(30, 3, '_________________ Firma y sello', 0, 'C', 0)


        self.set_line_width(0.3)  # Grosor del borde
        self.set_draw_color(0, 0, 0)  # Color del borde (negro)
        self.rect(10, 70, tarjeta_ancho_pts, tarjeta_alto_pts)  # Dibujar rectángulo
        self.set_xy(15, 75)
        self.set_font('Arial', '', 9)
        self.set_text_color(40, 40, 40)
        self.cell(75.60, 5, 'Importante', 0, 0, 'C', 0)
        self.set_draw_color(189, 13, 19)
        self.set_line_width(0.6)
        self.line(15.5, 81, 90.5, 81)
        self.set_xy(15, 83)
        self.set_font('Arial', '', 6)
        self.set_text_color(40, 40, 40)
        self.multi_cell(75.60, 3, '1. Conserve esta tarjeta y llévela siempre con su documentación personal', 0, '', 0)
        self.set_xy(15, 87)
        self.multi_cell(75.60, 3, '2. En ella se identifica grupo sanguíneo y Factor RH; y es de gran utilidad en caso de necesitar transfusión', 0, '', 0)
        self.set_xy(15, 93)
        self.multi_cell(75.60, 3, '3. Los datos en ella contenidos son permanentes y no cambian en el curso de la vida', 0, '', 0)

        self.image('gui/reportes/img/logo.png', x=47, y=98, w=8)

        self.set_xy(15, 110)
        self.set_font('Arial', 'B', 12)
        self.set_text_color(40, 40, 40)
        self.multi_cell(75.60, 5, 'La mejor transfusión es la que no se administra', 0, 'C', 0)





# Crear un objeto PDF con tamaño A4
pdf = TarjetaPDF()
pdf.add_page()

# Guardar el PDF en un archivo
pdf.output("Carnet.pdf")
print("Documento guardado con éxito.")
