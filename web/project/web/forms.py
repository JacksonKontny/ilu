# project/recipes/forms.py

from project import db
from flask_wtf import Form
from wtforms import validators, StringField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, NumberRange

from project.models import User
from sqlalchemy import or_


class RegistrationForm(Form):
    username = StringField('username', [validators.Length(min=8, max=64)])
    email = StringField('email', [validators.DataRequired(), validators.Email()])
    password = StringField('password', [validators.Length(min=8, max=64), validators.DataRequired()])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise validators.ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise validators.ValidationError('Please use a different email address.')

class SOForm(Form):
    email = StringField('email', [validators.Email()])
    username = StringField('username', [validators.Length(min=8, max=64)])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user_match_count = db.session.query(User).filter(
            (User.username == self.username.data) | (User.email == self.email.data)
        ).count()

        if user_match_count != 1 and not self.email.data:
            raise validators.ValidationError(
                'Please provide an existing username or a new email address')
