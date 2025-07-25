from flask import Flask
from flask_mysqldb import MySQL
from .config import Config  # Import your config class

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    
    # Load configuration from Config class
    app.config.from_object(Config)

    # Initialize MySQL with app
    mysql.init_app(app)

    # Import and register Blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
