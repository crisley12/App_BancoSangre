from fpdf import FPDF
from datetime import datetime
from pymongo import MongoClient

# Realizar la conexión a la base de datos
client = MongoClient('localhost', 27017)
database = client['banco_de_sangre']
users_collection = database['users']
users = users_collection.find()

# Clase PDF que hereda de FPDF
class PDF(FPDF):
    # Cabecera de página
    def header(self):
        self.image('gui/reportes/img/Logo.jpg', 10, 10, 70)
        self.set_xy(150, 10)
        self.set_font('Arial', '', 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(50, 3, 'Tlf: 0416-5029813\nbasantranfs@gmail.com', 0, 'R')

        self.set_xy(10, 60)
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(250, 250, 250)
        self.set_text_color(40, 40, 40)
        self.set_draw_color(255,255,255)
        self.set_line_width(0.5)
        self.cell(12, 10, 'Nro', 1, 0, 'C', 0)
        self.cell(48, 10, 'Email', 1, 0, 'C', 1)
        self.cell(45, 10, 'Cedula', 1, 0, 'C', 1)
        self.cell(35, 10, 'Rol', 1, 0, 'C', 1)
        self.cell(50, 10, 'ID', 1, 1, 'C', 1)
        self.set_draw_color(189, 13, 19)
        self.set_line_width(0.6)
        self.line(10.5, self.get_y(), 200, self.get_y())

    # Pie de página
    def footer(self):
        self.set_y(-27)
        self.set_font('Arial', '', 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 4, 'AV. LOS AGUSTINOS ESQUINA CALLE 1 N°1-245 BARRIO SANTA CECILIA, QUINTA LA MILAGROSA, SAN CRISTÓBAL - EDO. TACHIRA', 0, 'C', 0)
        self.set_xy(190, -20)
        self.cell(0, 10, str(self.page_no()) + '/{nb}', 0, 0, '')


# Crear un objeto PDF
pdf = PDF()
pdf.alias_nb_pages()
pdf.add_page()
pdf.set_font('Arial', '', 10)
pdf.set_xy(9, 30)
pdf.cell(10, 10, 'Fecha: ' + datetime.now().strftime('%d/%m/%Y'), 0, 0, 'L')
pdf.set_xy(120, 30)
pdf.cell(10, 10, 'Hora: ' + datetime.now().strftime('%I:%M %p'), 0, 0, 'L')
pdf.set_xy(90, 40)
pdf.set_font('Arial', 'B', 14)
pdf.cell(10, 15, "Usuarios", 0, 0, 'L')
pdf.ln(2)
pdf.set_draw_color(189, 13, 19)
pdf.set_line_width(1)
pdf.line(10, pdf.get_y() + 10, 200, pdf.get_y() + 10)

pdf.set_xy(10, 71)
pdf.set_font('Arial', '', 12)
pdf.set_fill_color(245, 245, 245)
pdf.set_text_color(40, 40, 40)
pdf.set_draw_color(255, 255, 255)
pdf.set_line_width(0.5)

# Iterar sobre los registros obtenidos de la base de datos
for user in users:
    email = user['email']
    cedula = user['paciente_id']
    role = user['role_id']
    user_id = user['id_usuario']

    pdf.cell(12, 10, str(user_id), 1, 0, 'C', 0)
    pdf.cell(48, 10, email, 1, 0, 'C', 1)
    pdf.cell(45, 10, cedula, 1, 0, 'C', 1)
    pdf.cell(35, 10, role, 1, 0, 'C', 1)
    pdf.cell(50, 10, str(user_id), 1, 1, 'C', 1)

# Guardar el PDF en un archivo
pdf.output("Usuarios.pdf")
print("Documento guardado con exito...")
