from flask import Flask
#from api.routers.auth_routes import auth_routes
from gui import main

app = Flask(__name__)
#app.register_blueprint(auth_routes)

if __name__ == '__main__':
    app.run()
    main.run_kivy_app()