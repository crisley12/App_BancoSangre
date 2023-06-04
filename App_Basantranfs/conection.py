from pymongo import MongoClient

# Configuración de la conexión
#client = MongoClient('mongodb://localhost:27017/')
#db = client['banco_de_sangre']
#users_collection = db["users"]

class Database:
    def __init__(self, host='localhost', port=27017, database_name=None):
        self.client = MongoClient(host, port)
        self.database = self.client[database_name]

    def get_collection(self, collection_name):
        return self.database[collection_name]