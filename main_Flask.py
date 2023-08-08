from flask import Flask, request,  jsonify, Response, session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId
# import requests
import traceback

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = 'admin123'
app.config['MONGO_URI'] = 'mongodb://localhost/banco_de_sangre'

mongo = PyMongo(app)


@app.route('/', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')


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

            # Obtener el ID del rol asociado al usuario
            role_id = user.get('role_id')
            if not role_id:
                # Si no se encuentra el role_id, el usuario no es válido
                return jsonify({'message': 'Usuario o contraseña incorrecto.'}), 401

            # Buscar el rol en la base de datos
            role = mongo.db.roles.find_one({'_id': role_id})
            role_name = role.get('nombre')

            # Guardar el user_id en la sesión
            session['user_id'] = user_id

            if role_name == 'paciente':
                # Buscar el paciente relacionado con el usuario
                paciente_id = user.get('paciente_id')
                if paciente_id:
                    paciente = mongo.db.pacientes.find_one({'_id': paciente_id})
                    print("Datos del paciente:")
                    print("Nombre:", paciente['p_nombre'])
                    print("Tipo de sangre:", paciente['t_sangre'])
                    response = {
                        'user_id': user_id,
                        'email': user['email'],
                        'password': user['password'],
                        'paciente': {
                            'nombre': paciente['p_nombre'],
                            'apellido': paciente['p_apellido'],
                            'tipo_sangre': paciente['t_sangre']
                        },
                        'role': role_name
                    }
                    return jsonify(response), 200
                else:
                    return jsonify({'message': 'Usuario o contraseña incorrecto.'}), 401

            elif role_name == 'medico':
                
                response = {
                    'user_id': user_id,
                    'email': user['email'],
                    'password': user['password'],
                    'role': role_name
                }
                return jsonify(response), 200
                # Lógica para buscar y obtener los datos específicos del médico
                # ...

            elif role_name == 'administrador':
                
                response = {
                    'user_id': user_id,
                    'email': user['email'],
                    'password': user['password'],
                    'role': role_name
                }
                return jsonify(response), 200
                # Lógica para buscar y obtener los datos específicos del administrador
                # ...

            else:
                return jsonify({'message': 'Usuario o contraseña incorrecto.'}), 401

    return jsonify({'message': 'Usuario o contraseña incorrecto.'}), 401


# Ruta de registro de usuario
@app.route('/registro_paciente', methods=['POST'])
def registro_paciente():
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
                    'f_nacimiento': f_nacimiento,
                    'eliminado': False
                }).inserted_id

                if paciente_id:
                    # Obtener la colección de roles
                    roles_collection = mongo.db.roles

                    # Buscar el rol "paciente"
                    paciente_role = roles_collection.find_one(
                        {'nombre': 'paciente'})

                    if not paciente_role:
                        # Si el rol "paciente" no existe, se crea
                        paciente_role_id = roles_collection.insert_one(
                            {'nombre': 'paciente'}).inserted_id
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
    

@app.route('/registro_medico', methods=['POST'])
def registro_medico():
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
        medico_collection = mongo.db.medico
        existing_medico = medico_collection.find_one({'cedula': cedula})
        if existing_medico:
            return jsonify({'error': 'El medico ya existe.'}), 409
        else:
            try:
                # Insertar el paciente en la colección "pacientes"
                medico_id = medico_collection.insert_one({
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

                if medico_id:
                    # Obtener la colección de roles
                    roles_collection = mongo.db.roles

                    # Buscar el rol "medico"
                    medico_role = roles_collection.find_one(
                        {'nombre': 'medico'})

                    if not medico_role:
                        # Si el rol "medico" no existe, se crea
                        medico_role_id = roles_collection.insert_one(
                            {'nombre': 'medico'}).inserted_id
                    else:
                        medico_role_id = medico_role['_id']

                    # Obtener la colección de usuarios
                    users_collection = mongo.db.users

                    hashed_password = generate_password_hash(password)

                    # Insertar el usuario en la colección "users" con referencia al paciente correspondiente
                    user_id = users_collection.insert_one({
                        'email': email,
                        'password': hashed_password,
                        'medico_id': medico_id,
                        'role_id': medico_role_id
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
    
    
@app.route('/registro_admin', methods=['POST'])
def registro_admin():
    data = request.get_json()
    p_nombre = data.get('p_nombre')
    email = data.get('email')
    password = data.get('password')

    if  p_nombre and email and password:
        # Verificar si el admin ya existe en la base de datos
        admin_collection = mongo.db.admin
        existing_admin = admin_collection.find_one({'p_nombre': p_nombre})
        if existing_admin:
            return jsonify({'error': 'El administrador ya existe.'}), 409
        else:
            try:
                # Insertar el paciente en la colección "pacientes"
                medico_id = admin_collection.insert_one({
                    'p_nombre': p_nombre,
                }).inserted_id

                if medico_id:
                    # Obtener la colección de roles
                    roles_collection = mongo.db.roles

                    # Buscar el rol "medico"
                    medico_role = roles_collection.find_one(
                        {'nombre': 'medico'})

                    if not medico_role:
                        # Si el rol "medico" no existe, se crea
                        medico_role_id = roles_collection.insert_one(
                            {'nombre': 'medico'}).inserted_id
                    else:
                        medico_role_id = medico_role['_id']

                    # Obtener la colección de usuarios
                    users_collection = mongo.db.users

                    hashed_password = generate_password_hash(password)

                    # Insertar el usuario en la colección "users" con referencia al paciente correspondiente
                    user_id = users_collection.insert_one({
                        'email': email,
                        'password': hashed_password,
                        'medico_id': medico_id,
                        'role_id': medico_role_id
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
 

@app.route('/eliminar_paciente/<string:paciente_id>', methods=['POST'])
def eliminar_paciente(paciente_id):
    # Restar 1 al índice para obtener el paciente correcto
    print(f"Recibiendo solicitud de eliminación para el paciente con ID: {paciente_id}")

    pacientes_collection = mongo.db.pacientes
    paciente = pacientes_collection.find_one({'_id': ObjectId(paciente_id)})

    if paciente:
        # Verificar si el paciente ya ha sido eliminado (eliminación lógica)
        if paciente.get('eliminado', False):
            return jsonify({'message': 'El paciente ya ha sido eliminado.'}), 400

        # Realizar la eliminación lógica, estableciendo el campo "eliminado" en True
        pacientes_collection.update_one({'_id': ObjectId(paciente_id)}, {'$set': {'eliminado': True}})
        return jsonify({'message': 'Paciente eliminado exitosamente.'}), 200
    else:
        return jsonify({'message': 'Paciente no encontrado.'}), 404

 


@app.route('/obtener_pacientes', methods=['GET'])
def obtener_pacientes():
    pacientes_collection = mongo.db.pacientes
    pacientes = pacientes_collection.find({'eliminado': {'$ne': True}})
    
    
    # Crear una lista para almacenar los datos de los pacientes
    datos_pacientes = []
    for paciente in pacientes:
        datos_paciente = {
            'id': str(paciente['_id']), 
            'cedula': paciente['cedula'],
            'nombre_completo': f"{paciente['p_apellido']} {paciente['p_nombre']}",
            'fecha_nacimiento': paciente['f_nacimiento'],
            'sexo': paciente['t_sexo'],
            'tipo_sangre': paciente['t_sangre'],
            'telefono': paciente['n_telefono'],
            #'eliminado': paciente.get('eliminado', False),
            'selected': False
            #'eliminar_url': f"/eliminar_paciente/{str(paciente['_id'])}"  # Agregar la URL de eliminación
        }
        datos_pacientes.append(datos_paciente)
        
    print("Datos de pacientes obtenidos:", datos_pacientes)

    return jsonify(datos_pacientes), 200


# mostrar
#@app.route('/user/<id>', methods=['GET'])
#def get_user(id):
 #   user = mongo.db.users.find_one({'_id': ObjectId(id)})
  #  response = json_util.dumps(user)
   # return response


# actualizar
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    if username and password and email:
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': {
            'username': username,
            'password': hashed_password,
            'email': email
        }})
        response = jsonify({'message': 'user' + id + 'fue actualizado'})
        return response




@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'resource not found' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response


if __name__ == '__main__':
    app.run(debug=True, port=5000)
