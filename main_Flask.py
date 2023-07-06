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

@app.route('/users', methods=['GET'])

def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')

# Ruta de registro de usuario
@app.route('/users/create', methods=['POST'])
def create_user():
    cedula = request.json['cedula']
    p_apellido = request.json['p_apellido']
    s_apellido = request.json['s_apellido']
    p_nombre = request.json['p_nombre']
    s_nombre = request.json['s_nombre']
    n_telefono = request.json['n_telefono']
    t_sangre = request.json['t_sangre']
    t_sexo = request.json['t_sexo']
    f_nacimiento = request.json['f_nacimiento']
    password = request.json['password']
    email = request.json['email']
    
# Verificar si los campos están vacíos
    campo_vacio = []
    if not cedula:
        campo_vacio.append("cedula")
    if not p_apellido:
        campo_vacio.append("p_apellido")
    if not s_apellido:
        campo_vacio.append("s_apellido")
    if not p_nombre:
        campo_vacio.append("p_nombre")
    if not s_nombre:
        campo_vacio.append("s_nombre")
    if not n_telefono:
        campo_vacio.append("n_telefono")
    if not t_sangre:
        campo_vacio.append("t_sangre")
    if not t_sexo:
        campo_vacio.append("t_sexo")
    if not f_nacimiento:
        campo_vacio.append("f_nacimiento")
    if not email:
        campo_vacio.append("email")
    if not password:
        campo_vacio.append("password")
          
    if campo_vacio:
        campos_str = ", ".join(campo_vacio)
        mensaje = f"Por favor, complete los siguientes campos: {campos_str}"
        return jsonify({'message':mensaje}), 409
    
# Verificar si el usuario ya existe en la base de datos
    existing_user = mongo.db.users.find_one({'cedula': cedula})
    if existing_user:
        return jsonify({'message': 'El usuario ya existe.'}), 420

    # Crear hash de la contraseña
    hashed_password = generate_password_hash(password)
    
    id = mongo.db.users.insert_one({'cedula': cedula, 
    'p_apellido': p_apellido, 's_apellido': s_apellido, 'p_nombre': p_nombre, 's_nombre': s_nombre,
    'n_telefono': n_telefono, 't_sangre': t_sangre,'t_sexo': t_sexo,
    'f_nacimiento': f_nacimiento, 'email': email, 'password': hashed_password})
                
        
    response = {
        'id': str(id),
        'cedula': cedula,
        'p_apellido': p_apellido,
        's_apellido': s_apellido,
        'p_nombre':    p_nombre,
        's_nombre':   s_nombre,
        'n_telefono':  n_telefono,
        't_sangre':   t_sangre,
        't_sexo':     t_sexo,
        'f_nacimiento':f_nacimiento,
        'email':        email,
        'password': hashed_password
    }
        
    return jsonify(response, {'message': 'Registro exictoso.'}), 201

#return jsonify({'message': 'Datos insuficientes.'}), 400

# Ruta de inicio de sesión
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

@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message':'resource not found' + request.url,
        'status': 404
    })
    response.status_code = 404 
    return response

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)