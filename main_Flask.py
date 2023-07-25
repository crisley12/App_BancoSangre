from flask import Flask, request,  jsonify, Response, session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId
# import requests

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

            # Guardar el user_id en la sesión
            session['user_id'] = user_id
            # Buscar el paciente relacionado con el usuario
            paciente_id = user.get('paciente_id')
            if paciente_id:
                paciente = mongo.db.pacientes.find_one({'_id': paciente_id})

                # Obtener las donaciones vinculadas con el paciente
                donaciones_collection = mongo.db.donaciones
                donaciones = donaciones_collection.find({'paciente_id': paciente_id})
                datos_donaciones = []
                for donacion in donaciones:
                    datos_donacion = {
                        'localidad': donacion['localidad'],
                        'numero_bolsa': donacion['numero_bolsa'],
                        'hemoglobina': donacion['hemoglobina'],
                        'volumen': donacion['volumen'],
                        'fecha_hora': donacion['fecha_hora'],
                        'paciente_id': donacion['paciente_id']
                    }
                    datos_donaciones.append(datos_donacion)

                # Agregar los datos del paciente y las donaciones a un solo diccionario
                response = {
                    'user_id': user_id,
                    'email': user['email'],
                    'password': user['password'],
                    'donaciones': datos_donaciones,
                    'paciente': {
                        'nombre': paciente['p_nombre'],
                        'apellido': paciente['p_apellido'],
                        'tipo_sangre': paciente['t_sangre']
                    },
                }
                print("Datos de las donaciones:", datos_donaciones)
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



# @app.route('/obtener_donaciones_paciente', methods=['GET'])
# def obtener_donaciones_paciente():
#     # Obtener el ID del paciente desde la sesión
#     paciente_id = session.get('paciente_id')

#     if paciente_id:
#         # Buscar las donaciones vinculadas con el paciente en la base de datos
#         donaciones_collection = mongo.db.donaciones
#         donaciones = donaciones_collection.find({'paciente_id': paciente_id})

#         datos_donaciones = []
#         for donacion in donaciones:
#             datos_donacion = {
#                 'localidad': donacion['localidad'],
#                 'numero_bolsa': donacion['numero_bolsa'],
#                 'hemoglobina': donacion['hemoglobina'],
#                 'volumen': donacion['volumen'],
#                 'fecha_hora': donacion['fecha_hora'],
#                 'paciente_id': donacion['paciente_id']
#             }
#             datos_donaciones.append(datos_donacion)

#         return jsonify(datos_donaciones), 200
#     else:
#         return jsonify({'message': 'Usuario no autenticado o no vinculado con un paciente.'}), 401




@app.route('/obtener_pacientes', methods=['GET'])
def obtener_pacientes():
    pacientes_collection = mongo.db.pacientes
    pacientes = pacientes_collection.find()

    # Crear una lista para almacenar los datos de los pacientes
    datos_pacientes = []
    for paciente in pacientes:
        datos_paciente = {
            'paciente_id': str(paciente['_id']),
            'cedula': paciente['cedula'],
            'nombre_completo': f"{paciente['p_nombre']} {paciente['s_nombre']}",
            'apellido_completo': f"{paciente['p_apellido']} {paciente['s_apellido']}",
            'fecha_nacimiento': paciente['f_nacimiento'],
            'sexo': paciente['t_sexo'],
            'tipo_sangre': paciente['t_sangre'],
            'telefono': paciente['n_telefono']
        }
        datos_pacientes.append(datos_paciente)

    return jsonify(datos_pacientes), 200


@app.route('/actualizar_paciente/<id>', methods=['PUT'])
def actualizar_paciente(id):
    # Obtener los datos actualizados del paciente desde la solicitud JSON.
    data_actualizada = request.get_json()

    # Eliminar el campo 'role_id' si existe en los datos actualizados para evitar modificar el rol.
    if 'role_id' in data_actualizada:
        del data_actualizada['role_id']

    # Realiza las acciones de actualización en la base de datos.
    # Por ejemplo, si estás usando PyMongo, puedes realizar lo siguiente:
    pacientes_collection = mongo.db.pacientes
    paciente = pacientes_collection.find_one({'_id': ObjectId(id)})

    if paciente:
        # Aquí debes realizar todas las acciones necesarias para actualizar los datos del paciente
        # sin modificar el rol en la colección correspondiente.
        # Por simplicidad, en este ejemplo se devuelve un mensaje ficticio de éxito.
        # Supongamos que también actualizas los datos según los datos actualizados.
        # pacientes_collection.update_one({'_id': ObjectId(id)}, {'$set': data_actualizada})
        # Actualizar otros datos del paciente según los datos actualizados.

        return jsonify({"message": "Paciente actualizado exitosamente"}), 200
    else:
        return jsonify({"message": "Paciente no encontrado"}), 404


@app.route('/eliminar_paciente/<id>', methods=['DELETE'])
def eliminar_paciente(id):
    # Realiza las acciones de eliminación en la base de datos.
    # Por ejemplo, si estás usando PyMongo, puedes realizar lo siguiente:
    pacientes_collection = mongo.db.pacientes
    paciente = pacientes_collection.find_one({'_id': ObjectId(id)})

    if paciente:
        # Aquí debes realizar todas las acciones necesarias para eliminar el paciente
        # y sus datos relacionados de las colecciones correspondientes.
        # Por simplicidad, en este ejemplo se devuelve un mensaje ficticio de éxito.
        # Supongamos que también eliminas los datos relacionados en las otras colecciones.
        # pacientes_collection.delete_one({'_id': ObjectId(id)})
        # Eliminar datos relacionados en otras colecciones según la lógica de tu aplicación.

        return jsonify({"message": "Paciente eliminado exitosamente"}), 200
    else:
        return jsonify({"message": "Paciente no encontrado"}), 404




@app.route('/buscar_pacientes_por_cedula', methods=['POST'])
def buscar_pacientes_por_cedula():
    data = request.get_json()
    cedula = data.get('cedula')

    if cedula:
        # Realiza la búsqueda de pacientes por cédula en la base de datos
        pacientes_collection = mongo.db.pacientes
        paciente = pacientes_collection.find_one({'cedula': cedula})

        if paciente:
            # Si se encuentra el paciente, extraer su _id y otros datos
            paciente_id = str(paciente['_id'])
            p_nombre = paciente['p_nombre']
            p_apellido = paciente['p_apellido']

            # Crear un diccionario con los datos del paciente, incluyendo el _id
            datos_paciente = {
                'cedula': cedula,
                'p_nombre': p_nombre,
                'p_apellido': p_apellido,
                'paciente_id': paciente_id  # Agregar el _id del paciente al diccionario
            }

            return jsonify(datos_paciente), 200
        else:
            return jsonify({'error': 'No se encontró ningún paciente con esa cédula.'}), 404
    else:
        return jsonify({'error': 'Cédula no proporcionada en la solicitud.'}), 400



@app.route('/crear_donacion', methods=['POST'])
def crear_donacion():
    data = request.get_json()

    localidad = data.get('localidad')
    numero_bolsa = data.get('numero_bolsa')
    hemoglobina = data.get('hemoglobina')
    volumen = data.get('volumen')
    fecha_hora = data.get('fecha_hora')
    paciente_id = data.get('paciente_id')

    # Verificar si la colección "donaciones" existe en la base de datos
    if 'donaciones' not in mongo.db.list_collection_names():
        # Si no existe, crea la colección "donaciones"
        mongo.db.create_collection('donaciones')

    # Crear el documento de la donación
    donacion = {
        'localidad': localidad,
        'numero_bolsa': numero_bolsa,
        'hemoglobina': hemoglobina,
        'volumen': volumen,
        'fecha_hora': fecha_hora,
        'paciente_id': paciente_id
    }

    # Insertar el documento en la colección "donaciones"
    mongo.db['donaciones'].insert_one(donacion)

    return jsonify({'message': 'Donación registrada exitosamente.'}), 200



@app.route('/obtener_donaciones', methods=['GET'])
def obtener_donaciones():
    donaciones_collection = mongo.db.donaciones
    donaciones = donaciones_collection.find()

    datos_donaciones = []
    for donacion in donaciones:
        datos_donacion = {
            'localidad': donacion['localidad'],
            'numero_bolsa': donacion['numero_bolsa'],
            'hemoglobina': donacion['hemoglobina'],
            'volumen': donacion['volumen'],
            'fecha_hora': donacion['fecha_hora'],
            'paciente_id': donacion['paciente_id']
        }
        datos_donaciones.append(datos_donacion)

    return jsonify(datos_donaciones), 200




# mostrar
@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(user)
    return response


@app.route('/guardar_respuestas', methods=['POST'])
def guardar_respuestas():
    response = request.get_json()
    respuestas = response.get('respuestas')

    if respuestas:
        # Guardar las respuestas en la base de datos
        respuestas_collection = mongo.db.respuestas
        respuestas_id = respuestas_collection.insert_one(
            respuestas).inserted_id

        if respuestas_id:
            return jsonify({'message': 'Respuestas guardadas exitosamente.'}), 200
        else:
            return jsonify({'error': 'Error al guardar las respuestas.'}), 500
    else:
        return jsonify({'error': 'Respuestas no encontradas en la solicitud.'}), 400


# eliminar
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'user' + id + 'se borro'})
    print(id)
    return response

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


@app.route('/obtener_respuestas', methods=['GET'])
def obtener_respuestas():
    respuestas_collection = mongo.db.respuestas
    respuestas = respuestas_collection.find()
    response = json_util.dumps(respuestas)
    return Response(response, mimetype='application/json')


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
