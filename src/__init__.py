from flask import Flask
from flask_cors import CORS
from src.routes.ia_class import bp as ia_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(ia_bp)

    return app