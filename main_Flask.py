from flask import Flask, request,  jsonify, Response, session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId
#import requests

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = 'admin123'
app.config['MONGO_URI']='mongodb://localhost/banco_de_sangre'

mongo = PyMongo(app)

@app.route('/', methods=['GET'])

def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')


#Ruta de inicio de sesión
@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    
    if email and password:
        # Buscar el usuario en la base de datos
        user = mongo.db.users.find_one({'email': email})
        if user and check_password_hash(user['password'], password):
            user_id = str(user['_id'])
            
            # Guardar el user_id en la sesión
            session['user_id'] = user_id
            
            response = {
                'user_id': user_id,
                'email': user['email'],
                'password': user['password']
            }
            return jsonify(response), 200
        
    return jsonify({'message': 'Usuario o contraseña incorrecto.'}), 401


# Ruta de registro de usuario
@app.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    cedula = data.get('cedula')
    p_apellido = data.get('p_apellido')
    s_apellido = data.get('s_apellido')
    p_nombre = data.get('p_nombre')
    s_nombre = data.get('s_nombre')
    n_telefono = data.get('n_telefono')
    t_sangre = data.get('t_sangre')
    t_sexo = data.get('t_sexo')
    f_nacimiento = data.get('f_nacimiento')
    email = data.get('email')
    password = data.get('password')

    if cedula and p_apellido and s_apellido and p_nombre and s_nombre and n_telefono and t_sangre and t_sexo and f_nacimiento and email and password:
        # Verificar si el paciente ya existe en la base de datos
        pacientes_collection = mongo.db.pacientes
        existing_paciente = pacientes_collection.find_one({'cedula': cedula})
        if existing_paciente:
            return jsonify({'error': 'El paciente ya existe.'}), 409
        else:
            try:
                # Insertar el paciente en la colección "pacientes"
                paciente_id = pacientes_collection.insert_one({
                    'cedula': cedula,
                    'p_apellido': p_apellido,
                    's_apellido': s_apellido,
                    'p_nombre': p_nombre,
                    's_nombre': s_nombre,
                    'n_telefono': n_telefono,
                    't_sangre': t_sangre,
                    't_sexo': t_sexo,
                    'f_nacimiento': f_nacimiento
                }).inserted_id

                if paciente_id:
                    # Obtener la colección de roles
                    roles_collection = mongo.db.roles

                    # Buscar el rol "paciente"
                    paciente_role = roles_collection.find_one({'nombre': 'paciente'})

                    if not paciente_role:
                        # Si el rol "paciente" no existe, se crea
                        paciente_role_id = roles_collection.insert_one({'nombre': 'paciente'}).inserted_id
                    else:
                        paciente_role_id = paciente_role['_id']

                    # Obtener la colección de usuarios
                    users_collection = mongo.db.users

                    hashed_password = generate_password_hash(password)

                                        # Insertar el usuario en la colección "users" con referencia al paciente correspondiente
                    user_id = users_collection.insert_one({
                        'email': email,
                        'password': hashed_password,
                        'paciente_id': paciente_id,
                        'role_id': paciente_role_id
                    }).inserted_id

                    if user_id:
                        return jsonify({'message': 'Registro exitoso.'}), 201
                    else:
                        return jsonify({'error': 'Error al registrar el usuario.'}), 500
                else:
                    return jsonify({'error': 'Error al registrar el paciente.'}), 500
            except Exception as e:
                return jsonify({'error': 'Error al registrar.'}), 500
    else:
        return jsonify({'error': 'Datos insuficientes.'}), 400


#mostrar
@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(user)
    return response

#eliminar
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'user' + id + 'se borro'})
    print(id)
    return response

#actualizar
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    
    if username and password and email:
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': {
            'username':username,
            'password':hashed_password,
            'email':email
        }})
        response = jsonify({'message': 'user'+ id + 'fue actualizado'})
        return response
    
@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message':'resource not found' + request.url,
        'status': 404
    })
    response.status_code = 404 
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)