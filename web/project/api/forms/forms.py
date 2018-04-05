from project import db
from flask_wtf import Form
from wtforms import validators, StringField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, NumberRange

from project.models import User
from sqlalchemy import or_

class LoginForm(Form):
    email = StringField('email', [validators.Length(max=64), validators.DataRequired()])
    password = StringField('password', [validators.Length(min=8, max=64), validators.DataRequired()])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user_match_query = User.query.filter_by(
            email=self.email.data
        )

        user_match_count = user_match_query.count()

        if user_match_count != 1:
            self.email.errors.append(
                'We were unable to find that email in our system')
            return False

        user = user_match_query.first()

        if user and not user.check_password(self.password.data):
            self.password.errors.append(
                'The password you provided is incorrect')
            return False

        return True


class RegistrationForm(Form):
    email = StringField('email', [validators.DataRequired(), validators.Email()])
    password = StringField('password', [validators.Length(min=8, max=64), validators.DataRequired()])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data, is_temp=False).first()
        if user is not None:
            self.email.errors.append('Email already exists. Please use a different email address.')


class SOForm(Form):
    email = StringField('email', [validators.Email()])
