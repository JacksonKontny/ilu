import uuid
from project import db, bcrypt, app
from sqlalchemy_utils import URLType
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from datetime import datetime
from markdown import markdown
from flask import url_for
import bleach
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin

class User(UserMixin, db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    so_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_temp = db.Column(db.Boolean, default=False)
    given_name = db.Column(db.String(64))
    family_name = db.Column(db.String(64))
    picture_url = db.Column(URLType)
    gender = db.Column(db.String(16))

    @app.login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @classmethod
    def register_user(cls, registration_form):
        temp_user = cls.query.filter_by(
            email=registration_form.email.data,
            is_temp=True
        ).first()
        if temp_user:
            temp_user.save(registration_form.password.data)
            return False, temp_user
        user = User(
            email=registration_form.email.data
        )
        user.save(registration_form.password.data)
        return True, user

    def update_so(self, form):
        so = db.session.query(User).filter(
            User.email == form.email.data
        ).first()
        if not so:
            so = User(email=form.email.data, is_temp=True)
            so.save(password=str(uuid.uuid4()))
        self.so_id = so.id
        self.save()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self, password=None):
        if password:
            self.password_hash = generate_password_hash(password)
        db.session.add(self)
        db.session.commit()

    def has_so(self):
        if self.so_id:
            so = User.query.filter_by(id=self.so_id).first()
            return not so.is_temp
        return False

    def ping_so(self):
        msg = Ping(from_id=self.id, to_id=self.so_id)
        msg.save()
        return msg

    def sent_messages(self):
        return Ping.query.filter_by(from_id=self.id, to_id=self.so_id)

    def received_messages(self):
        return Ping.query.filter_by(from_id=self.so_id, to_id=self.id)

    def __repr__(self):
        if hasatter(self, 'email'):
            return '<User {}>'.format(self.email)
        return '<User {}>'.format(self.id)


class Ping(db.Model):

    __tablename__ = 'ping'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    from_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    to_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    datetime = db.Column(db.DateTime)

    def save(self):
        self.datetime = datetime.now()
        db.session.add(self)
        db.session.commit()
        db.session.expire(self)

    def serialize(self):
        return {
            'id': self.id,
            'sent_at': self.datetime
        }


class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)
