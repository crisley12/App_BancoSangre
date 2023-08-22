from flask import Flask, request,  jsonify, Response, session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId
# import requests
import traceback
import datetime

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
            user_role = user.get('role_id')  # Ajusta según cómo almacenas los roles en tu base de datos

            # Auditoría: Registrar el evento de inicio de sesión exitoso
            audit_event = {
                'event_type': 'login_exitoso',
                'user_id': user_id,
                'timestamp': datetime.datetime.now(),
                'details': {
                    'email': email,
                    'user_role': user_role
                }
            }
            mongo.db.auditoria_logs.insert_one(audit_event)

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

            # Buscar el paciente relacionado con el usuario
            if role_name == 'paciente':
                # Buscar el paciente relacionado con el usuario
                paciente_id = user.get('paciente_id')
                if paciente_id:
                    paciente = mongo.db.pacientes.find_one(
                        {'_id': paciente_id})

                    # Resto del código
                    response = {
                        'user_id': user_id,
                        'paciente_id': str(paciente_id),
                        'email': user['email'],
                        'password': user['password'],
                        'paciente': {
                            'nombre': paciente['p_nombre'],
                            'apellido': paciente['p_apellido'],
                            'tipo_sangre': paciente['t_sangre']
                        },
                        'role': role_name
                    }
                    print("Datos del paciente:", paciente)
                    print("Contenido de la sesión:", session)
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

            elif role_name == 'admin':

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

                """# Auditoría: Registrar el evento de inicio de sesión fallido
                audit_event = {
                    'event_type': 'login_fallido',
                    'user_id': None,  # Puedes ajustar esto según tus necesidades
                    'timestamp': datetime.datetime.now(),
                    'details': {
                    'email': email
                    }
                }
                
                mongo.db.auditoria_logs.insert_one(audit_event)"""

                return jsonify({'message': 'Usuario o contraseña incorrecto.'}), 401

    return jsonify({'message': 'Usuario o contraseña incorrecto.'}), 401


@app.route('/logout', methods=['POST'])
def logout():
    user_id = request.form.get('user_id')

    if user_id:
        session.clear()

        # Registrar el evento de logout en la colección de auditoría
        audit_event = {
            'event_type': 'logout',
            'user_id': user_id,
            'timestamp': datetime.datetime.now(),
            'details': {
                'user_id': user_id
            }
        }

        mongo.db.auditoria_logs.insert_one(audit_event)

        return jsonify({'message': 'Sesión cerrada exitosamente'}), 200
    else:
        return jsonify({'message': 'No hay sesión activa'}), 401



@app.route('/registro_paciente', methods=['POST'])
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
        pacientes_user_collection = mongo.db.users
        pacientes_collection = mongo.db.pacientes
        existing_email = pacientes_user_collection.find_one({'email': email})
        existing_cedula = pacientes_collection.find_one({'cedula': cedula})
        if existing_cedula or existing_email:
            return jsonify({'error': 'El paciente ya existe, cedula o email existentes'}), 409
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
                    # Auditoría: Registrar el evento de registro de paciente

                    audit_event = {
                        'event_type': 'Registro Paciente Nuevo',
                        'user_id': session.get('user_id'),
                        'timestamp': datetime.datetime.now(),
                        'details': {
                            'paciente_id': paciente_id,
                            'cedula': cedula,
                            'nombre_completo': f"{p_apellido} {p_nombre}"
                        }
                    }
                    mongo.db.auditoria_logs.insert_one(audit_event)

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
                 # Auditoría: Registrar el evento de error en el registro de paciente

                audit_event = {
                    'event_type': 'error_registro_paciente',
                    'user_id': session.get('user_id'),
                    'timestamp': datetime.datetime.now(),
                    'details': {
                        'error_message': str(e),
                        'traceback': traceback.format_exc()
                    }
                }
                mongo.db.auditoria_logs.insert_one(audit_event)

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
        medico_user_collection = mongo.db.users
        medico_collection = mongo.db.medico
        existing_email = medico_user_collection.find_one({'email': email})
        existing_cedula = medico_collection.find_one({'cedula': cedula})
        if existing_cedula or existing_email:
            return jsonify({'error': 'El medico ya existe, cedula o email existentes'}), 409
        else:
            try:
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
                    # Auditoría: Registrar el evento de registro de medico

                    audit_event = {
                        'event_type': 'registro_medico',
                        'user_id': session.get('user_id'),
                        'timestamp': datetime.datetime.now(),
                        'details': {
                            'medico_id': medico_id,
                            'cedula': cedula,
                            'nombre_completo': f"{p_apellido} {p_nombre}"
                        }
                    }
                    mongo.db.auditoria_logs.insert_one(audit_event)

                    # Obtener la colección de roles
                    roles_collection = mongo.db.roles

                    medico_role = roles_collection.find_one(
                        {'nombre': 'medico'})

                    if not medico_role:
                        medico_role_id = roles_collection.insert_one(
                            {'nombre': 'medico'}).inserted_id
                    else:
                        medico_role_id = medico_role['_id']

                    users_collection = mongo.db.users

                    hashed_password = generate_password_hash(password)

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

    if p_nombre and email and password:
        admin_collection = mongo.db.admin
        admin_user_collection = mongo.db.users
        existing_email = admin_user_collection.find_one({'email': email})
        existing_nombre = admin_collection.find_one({'p_nombre': p_nombre})
        if existing_nombre or existing_email:
            return jsonify({'error': 'El administrador ya existe.'}), 409
        else:
            try:
                admin_id = admin_collection.insert_one({
                    'p_nombre': p_nombre,
                }).inserted_id

                if admin_id:
                    # Auditoría: Registrar el evento de registro de paciente

                    audit_event = {
                        'event_type': 'registro_admin',
                        'user_id': session.get('user_id'),
                        'timestamp': datetime.datetime.now(),
                        'details': {
                            'medico_id': admin_id,
                            'email': email,
                            'nombre': f"{p_nombre}"
                        }
                    }
                    mongo.db.auditoria_logs.insert_one(audit_event)

                    # Obtener la colección de roles
                    roles_collection = mongo.db.roles

                    admin_role = roles_collection.find_one(
                        {'nombre': 'admin'})

                    if not admin_role:
                        admin_role_id = roles_collection.insert_one(
                            {'nombre': 'admin'}).inserted_id
                    else:
                        admin_role_id = admin_role['_id']

                    users_collection = mongo.db.users

                    hashed_password = generate_password_hash(password)

                    user_id = users_collection.insert_one({
                        'email': email,
                        'password': hashed_password,
                        'admin_id': admin_id,
                        'role_id': admin_role_id
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


@app.route('/donaciones_paciente', methods=['GET'])
def obtener_donaciones_paciente():
    paciente_id = request.args.get('paciente_id')

    if paciente_id:
        donaciones_collection = mongo.db.donaciones
        donaciones_cursor = donaciones_collection.find(
            {'paciente_id': paciente_id})
        datos_donaciones = []
        for donacion in donaciones_cursor:
            datos_donacion = {
                'localidad': donacion['localidad'],
                'numero_bolsa': donacion['numero_bolsa'],
                'hemoglobina': donacion['hemoglobina'],
                'volumen': donacion['volumen'],
                'fecha_hora': donacion['fecha_hora'],
                'paciente_id': str(donacion['paciente_id'])
            }
            datos_donaciones.append(datos_donacion)
            print(datos_donacion)
            print(datos_donaciones)

        return jsonify(datos_donaciones), 200

    return jsonify({'message': 'El parámetro paciente_id no se proporcionó.'}), 400


@app.route('/eliminar_paciente/<string:paciente_id>', methods=['POST'])
def eliminar_paciente(paciente_id):

    # Auditoría: Registrar el evento de solicitud de eliminación de paciente
    audit_event = {
        'event_type': 'solicitud_eliminar_paciente',
        'user_id': session.get('user_id'),
        'timestamp': datetime.datetime.now(),
        'details': {
            'paciente_id': paciente_id
        }
    }

    mongo.db.auditoria_logs.insert_one(audit_event)

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

        p_nombre = paciente.get('p_nombre')
        cedula = paciente.get('cedula')

        # Registrar el evento de eliminación en la colección de auditoría
        audit_event = {
            'event_type': 'Paciente eliminado',
            'user_id': session.get('user_id'),
            'timestamp': datetime.datetime.now(),
            'details': {
                'registro_tipo': 'paciente',  # O "medico" o "admin" según corresponda
                'cedula': cedula,  # Agregar otros detalles relevantes
                'nombre_completo': f"{p_nombre}"
            }
        }
        mongo.db.auditoria_logs.insert_one(audit_event)

        return jsonify({'message': 'Paciente eliminado exitosamente.'}), 200
    else:
        return jsonify({'message': 'Paciente no encontrado.'}), 404

 


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
            'telefono': paciente['n_telefono'],
            #'eliminado': paciente.get('eliminado', False),
            'selected': False
            #'eliminar_url': f"/eliminar_paciente/{str(paciente['_id'])}"  # Agregar la URL de eliminación
        }
        datos_pacientes.append(datos_paciente)
        
    print("Datos de pacientes obtenidos:", datos_pacientes)

    return jsonify(datos_pacientes), 200


@app.route('/buscar_pacientes_por_cedula', methods=['POST'])
def buscar_pacientes_por_cedula():
    data = request.get_json()
    cedula = data.get('cedula')

    if cedula:
        pacientes_collection = mongo.db.pacientes
        paciente = pacientes_collection.find_one({'cedula': cedula})       

        if paciente:

            # Registrar el evento de búsqueda de paciente por cédula en la colección de auditoría
            audit_event = {
                'event_type': 'Busqueda de paciente',
                'user_id': session.get('user_id'),
                'timestamp': datetime.datetime.now(),
                'details': {
                    'cedula_busqueda': cedula,
                    'paciente_encontrado': paciente['_id']
                }
            }
            mongo.db.auditoria_logs.insert_one(audit_event)

            paciente_id = str(paciente['_id'])
            p_nombre = paciente['p_nombre']
            p_apellido = paciente['p_apellido']

            datos_paciente = {
                'cedula': cedula,
                'p_nombre': p_nombre,
                'p_apellido': p_apellido,
                'paciente_id': paciente_id
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

    if 'donaciones' not in mongo.db.list_collection_names():
        mongo.db.create_collection('donaciones')

    donacion = {
        'localidad': localidad,
        'numero_bolsa': numero_bolsa,
        'hemoglobina': hemoglobina,
        'volumen': volumen,
        'fecha_hora': fecha_hora,
        'paciente_id': paciente_id
    }

    mongo.db['donaciones'].insert_one(donacion)

    # Registrar el evento de agregación de donación en la colección de auditoría
    audit_event = {
        'event_type': 'Nueva Donacion',
        'user_id': session.get('user_id'),
        'timestamp': datetime.datetime.now(),
        'details': {
            'localidad': localidad,
            'numero_bolsa': numero_bolsa,
            'hemoglobina': hemoglobina,
            'volumen': volumen,
            'fecha_hora': fecha_hora,
            'paciente_id': paciente_id
        }
    }
    mongo.db.auditoria_logs.insert_one(audit_event)

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


@app.route('/obtener_usuarios', methods=['GET'])
def obtener_usuarios():
    usuarios_collection = mongo.db.users
    roles_collection = mongo.db.roles
    paciente_collection = mongo.db.pacientes

    usuarios = usuarios_collection.find()

    datos_usuarios = []
    for usuario in usuarios:
        paciente_id = usuario.get('paciente_id')
        if paciente_id:
            paciente = paciente_collection.find_one(
                {'_id': ObjectId(paciente_id)})
            if paciente:
                cedula_paciente = paciente['cedula']
            else:
                cedula_paciente = "Paciente no encontrado"
        else:
            cedula_paciente = "No asignado"

        role_id = usuario.get('role_id')
        if role_id:
            rol = roles_collection.find_one({'_id': ObjectId(role_id)})
            if rol:
                nombre_rol = rol['nombre']
            else:
                nombre_rol = "Rol no encontrado"
        else:
            nombre_rol = "No asignado"

        datos_usuario = {
            'email': usuario['email'],
            'paciente_id': cedula_paciente,
            'id_usuario': str(usuario['_id']),
            'role_id': nombre_rol,
        }
        datos_usuarios.append(datos_usuario)

    return jsonify(datos_usuarios), 200


@app.route('/obtener_medicos', methods=['GET'])
def obtener_medicos():
    medicos_collection = mongo.db.medico
    medicos = medicos_collection.find()

    datos_medicos = []
    for medico in medicos:
        datos_medico = {
            'paciente_id': str(medico['_id']),
            'cedula': medico['cedula'],
            'nombre_completo': f"{medico['p_nombre']} {medico['s_nombre']}",
            'apellido_completo': f"{medico['p_apellido']} {medico['s_apellido']}",
            'fecha_nacimiento': medico['f_nacimiento'],
            'sexo': medico['t_sexo'],
            'tipo_sangre': medico['t_sangre'],
            'telefono': medico['n_telefono']
        }
        datos_medicos.append(datos_medico)

    return jsonify(datos_medicos), 200


# mostrar
#@app.route('/user/<id>', methods=['GET'])
#def get_user(id):
 #   user = mongo.db.users.find_one({'_id': ObjectId(id)})
  #  response = json_util.dumps(user)
   # return response


# eliminar
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = mongo.db.users.delete_one({'_id': ObjectId(id)})
    if user:
        # Registrar el evento de eliminación de usuario en la colección de auditoría
        audit_event = {
            'event_type': 'Usuario eliminado',
            'user_id': session.get('user_id'),
            'timestamp': datetime.datetime.now(),
            'details': {
                'user_id': str(user['_id']),
                'username': user['username'],
                'email': user['email']
            }
        }
        mongo.db.auditoria_logs.insert_one(audit_event)

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
        user = mongo.db.users.find_one({'_id': ObjectId(id)})
        if user:
        # Capturar los detalles del usuario antes de la edición
            old_username = user.get('username')
            old_email = user.get('email')
            # Registrar el evento de actualización de usuario en la colección de auditoría
            audit_event = {
                'event_type': 'Usuario Actualizado',
                'user_id': session.get('user_id'),
                'timestamp': datetime.datetime.now(),
                'details': {
                    'user_id': str(user['_id']),
                    'username_anterior': user['username'],
                    'email_anterior': user['email'],
                    'username_nuevo': username,
                    'email_nuevo': email
                }
            }
            mongo.db.auditoria_logs.insert_one(audit_event)

        # Actualizar el usuario en la base de datos
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': {
            'username': username,
            'password': hashed_password,
            'email': email
        }})

         # Registrar la auditoría de edición de usuario
        audit_event = {
            'event_type': 'edicion_usuario',
            'user_id': session.get('user_id'),  # Ajusta según cómo obtienes el ID del usuario actual
            'timestamp': datetime.datetime.now(),
            'details': {
                'edited_user_id': str(user['_id']),
                'old_username': old_username,
                'new_username': username,
                'old_email': old_email,
                'new_email': email
                }
            }
        mongo.db.auditoria_logs.insert_one(audit_event)

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
