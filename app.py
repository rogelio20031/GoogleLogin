from flask import Flask, redirect, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from oauthlib.oauth2 import WebApplicationClient
from models import User_info
import requests
from db import init_db
import os
import json
from dotenv import load_dotenv
load_dotenv()

#Credenciales del proyecto de Google obtenidas desde variables de entorno locales
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

init_db(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.unauthorized_handler
def unauthorized():
    return "Necesitas estar logeado para acceder a este contenido", 403


client = WebApplicationClient(GOOGLE_CLIENT_ID)

@login_manager.user_loader
def load_user(user_id):
    return User_info.get(user_id)

#Ruta main
@app.route("/")
def index():
    """
    Hay dos posibilidades, que el usuario ya esté autenticado y que no, dependiendo de esto es lo que va a mostrar
    :return: No autenticado - Botón de logearse
    :return: Autenticado - Información de la persona
    """
    if current_user.is_authenticated:
        return(
            "<p>Hola, {}! Estas logeando con este email: {}</p>"
            "<div><p>Foto de perfil de google:</p>"
            '<img src="{}" alt="Foto de perfil de google"></img></div>'
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.name, current_user.email, current_user.profile_pic
            )
        )
    else:
        return '<a class="button" href="/login">Google Login</a>'

@app.route("/login")
def login():
    """
    Redirige al usuario a Google para iniciar sesión, primero obtenemos la URL de autorización de Google, luego
    construimos una URL personalizada con el id y ajustamos que permisos vamos a pedir (scope)
    :return: Redirigimos al usuario con la URL de Google que creamos
    """
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid","email","profile"]
    )
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    """
    Procesa la respuesta de Google después del login, primero obtenemos el código que manda Google, pedimos un access
    token a Google utilizando este código, con este token pedimos la información del usuario, si el correo del usuario
    está verificado creamos el usuario en la base de datos (si aún no existe) si el correo no está verificado muestra
    un error
    :return: Redirigimos al usuario al inicio
    """
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "El email no está disponible o no está verificado por google",400

    user = User_info(id=unique_id, name=users_name, email=users_email, profile_pic=picture)

    if not User_info.get(unique_id):
        User_info.create(unique_id, users_name, users_email, picture)

    login_user(user)
    return redirect(url_for("index"))

@app.route("/logout")
@login_required
def logout():
    """
    Cierra la sesión del usuario
    :return: Redirige al inicio
    """
    logout_user()
    return redirect(url_for("index"))

def get_google_provider_cfg():
    """
    Trae la configuración de Google OAuth haciendo una petición a la URL que proporcionamos
    :return: devuelve las URLs importantes como login, token, user info, etc. En formato JSON
    """
    return requests.get(GOOGLE_DISCOVERY_URL).json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)