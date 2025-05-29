from db import db
from flask_login import UserMixin


class User_info(db.Model, UserMixin):
    __tablename__ = 'USER_INFO'
    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    profile_pic = db.Column(db.Text(255), nullable=False)

    @staticmethod
    def get(user_id):
        """
        Obtiene el id del usuario (Si es que existe)
        :param user_id: id a buscar
        :return: información del usuario encontrada en la base de datos
        """
        return User_info.query.get(user_id)

    @staticmethod
    def create(id_, name, email, profile_pic):
        """
        Crea un usuario en la base de datos
        :param id_: id del usuario
        :param name: nombre del usuario
        :param email: correo del usuario
        :param profile_pic: foto de perfil del usuario
        :return: el usuario creado
        """
        user = User_info(id = id_, name = name, email = email,  profile_pic = profile_pic)
        db.session.add(user)
        db.session.commit()
        return user