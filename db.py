import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def get_database_uri():
    """
    Variables de conexion para la base de datos
    :return: Cadena completa para la conexion
    """
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASS", "NYVA")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "33060")
    dbname = os.getenv("DB_NAME", "google")
    return f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{dbname}"

def init_db(app):
    """
    Inicializacion de la base de datos con flask_sqlalchemy
    :param app: aplicacion de flask
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)