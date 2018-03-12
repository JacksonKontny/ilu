# project/recipes/forms.py

from project import db
from flask_wtf import Form
from wtforms import validators, StringField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, NumberRange

from project.models import User
from sqlalchemy import or_

class LoginForm(Form):
    login = StringField('username', [validators.Length(max=64)])
    password = StringField('password', [validators.Length(min=8, max=64), validators.DataRequired()])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user_match_query = db.session.query(User).filter(
            (User.username == self.login.data) | (User.email == self.login.data)
        )

        user_match_count = user_match_query.count()

        if user_match_count != 1:
            self.login.errors.append(
                'We were unable to find that username or email in our system')

        user = user_match_query.first()

        if not user.check_password(self.password.data):
            self.password.errors.append(
                'The password you provided is incorrect')

        return not self.login.errors and not self.password.errors


class RegistrationForm(Form):
    username = StringField('username', [validators.Length(min=8, max=64)])
    email = StringField('email', [validators.DataRequired(), validators.Email()])
    password = StringField('password', [validators.Length(min=8, max=64), validators.DataRequired()])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            self.username.errors.append('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            self.email.errors.append('Please use a different email address.')

class SOForm(Form):
    email = StringField('email', [validators.Email()])
    username = StringField('username')

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user_match_count = db.session.query(User).filter(
            (User.username == self.username.data) | (User.email == self.email.data)
        ).count()

        if user_match_count != 1 and not self.email.data:
            self.username.errors.append(
                'Please provide an existing username or a new email address')
            return False

        return True
