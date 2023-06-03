from pymongo import MongoClient

# Configuración de la conexión
client = MongoClient('mongodb://localhost:27017/')
db = client['banco_de_sangre']