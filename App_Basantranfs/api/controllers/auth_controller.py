from database.conection import db

class AuthController:
    def login(self, username, password):
        # Verificar las credenciales del usuario en la base de datos
        user = db.find_user(username)
        if user and user.password == password:
            return True
        return False

