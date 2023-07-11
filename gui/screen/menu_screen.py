from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from flask import session
from bson.objectid import ObjectId
from flask import current_app
from flask_pymongo import PyMongo


class MenuScreen(MDScreen):
    def __init__(self, **kwargs) -> None:
        Builder.load_file('screen_Kv/menu_screen.kv')
        super().__init__(**kwargs)

    def get_user_data(self):
        with current_app.app_context():
            mongo = PyMongo(current_app)
            user_id = session.get('user_id')
            if user_id:
                users = mongo.db.users
                paciente = users.find_one({'_id': ObjectId(user_id)})
                if paciente:
                    return paciente
            return None

    def show_user_data(self):
         with current_app.app_context():
            mongo = PyMongo(current_app)
            user_data = self.get_user_data()
            
            if user_data:
                paciente_id = user_data['paciente_id']
                pacientes = mongo.db.pacientes
                paciente = pacientes.find_one({'_id': ObjectId(paciente_id)})
                
                if paciente:
                    p_nombre_label = self.ids.p_nombre_label
                    t_sangre_label = self.ids.t_sangre_label

                    # Establecer los valores en los MDLabel
                    p_nombre_label.text = paciente['p_nombre']
                    t_sangre_label.text = paciente['t_sangre']
