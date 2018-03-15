from flask import Blueprint, request, jsonify
from flask_login import current_user, login_user, logout_user

from project import app
from project.api.forms.forms import LoginForm
from project.models import User


login_blueprint = Blueprint('login', __name__)


@login_blueprint.route('/login/', methods=['POST'])
def login():
    """Logs a user in

    Args:
        login (str): The user's username or email
        password (str): The user's non-hashed password

    Returns:
        200 - {'success': 'User <user_id> logged in'} if successful
        400 - {'error_field': ['field error1', 'field error2'...]..., }

    Notes:
        If the user is logged in, they will be logged out before logging them
        in to the requested username or email account.
    """
    if current_user.is_authenticated:
        logout_user()
    form = LoginForm()
    if form.validate():
        user = User.query.filter_by(username=form.login.data).first()
        login_user(user)
        response = jsonify({
            'success': 'User {} logged in'.format(user.id)
        })
        response.status_code = 200
        return response
    response = jsonify(form.errors)
    response.status_code = 400
    return response

@login_blueprint.route('/logout/')
def logout():
    """Logs a user out """
    logout_user()

    response = jsonify({
        'success': 'You have successfully logged out'
    })
    response.status_code = 200
    return response

