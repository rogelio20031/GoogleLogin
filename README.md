# Login con Google usando Flask + OAuth 2.0

Es un ejemplo que demuestra como implementar autenticación con google en
una aplicación web construida con **flask** utilizando **OAuth 2.0**.
Utiliza **MySQL** como base de datos y está preparado para ejecutarse
en contenedores Docker.

## Tecnologías utilizadas
- Python 3.11
- Flask
- OAuthLib / Requests-OAuthlib
- Flask-login
- MySQL
- Docker / Docker Compose

## Como ejecutar el proyecto

### 1. Clonar el repositorio

```bash
    git clone https://github.com/rogelio20031/GoogleLogin.git
```

### 2. Crear el archivo .env
Necesitas agregar el archivo .env en la raíz del proyecto
con las variables (Ajustalas según tus necesidades):
```bash
    GOOGLE_CLIENT_ID=clienteid
    GOOGLE_CLIENT_SECRET=clientsecret
```

### 3. Construir y ejecutar con Docker
```bash
  docker-compose up --build
```

Esto levanta la base de datos MySQL y la aplicación flask en el contenedor web
Puedes acceder a la app desde http://localhost:5000

## Endpoints principales
- / : Pagina principal
- /login : inicia el login con Google
- /login/callback : Callback que procesa la respuesta de Google
- /logout : Cierra sesión del usuario

## Flujo de autenticación
1. El usuario entra a / y da clic en "Google Login"
2. Es redirigido a Google para autorizar la app
3. Google redirige al callback con un code
4. Se obtiene un token de acceso
5. Se solicita la información del usuario
6. Se guarda en la base de datos y se inicia sesión

## Notas importantes
- redirect_uri debe coincidir exactamente en tu código y en la consola de Google
- Google requiere HTTPS en producción, pero en local puedes usar ssl_context="adhoc" en el run de flask
para pruebas
- El contenedor expone el puerto 5000 para el acceso


