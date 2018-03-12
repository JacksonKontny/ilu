from project import db, bcrypt, app
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from datetime import datetime
from markdown import markdown
from flask import url_for
import bleach
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):

    __tablename__ = 'user'

    user_id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    so_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    is_temp = db.Column(db.Boolean, default=False)

    @app.login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def check_password(self):
        return check_password_hash(self.password_hash, password)

    def save(self, password=None):
        if password:
            self.password_hash = generate_password_hash(password)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<User {}>'.format(self.username)
