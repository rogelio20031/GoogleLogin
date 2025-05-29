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
        return User_info.query.get(user_id)

    @staticmethod
    def create(id_, name, email, profile_pic):
        user = User_info(id = id_, name = name, email = email,  profile_pic = profile_pic)
        db.session.add(user)
        db.session.commit()
        return user