from flask import Blueprint, request, jsonify
from api.controllers.auth_controller import AuthController

auth_routes = Blueprint('auth_routes', __name__)
auth_controller = AuthController()

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if auth_controller.login(username, password):
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Invalid username or password'})