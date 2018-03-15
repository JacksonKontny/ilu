# project/api/views.py
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required, login_user, logout_user

from sqlalchemy.orm import load_only

from project import db, app
from project.api.forms import RegistrationForm, SOForm, LoginForm
from project.models import User


api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/login/', methods=['POST'])
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
    else:
        response = jsonify(form.errors)
        response.status_code = 400
        return response

@api_blueprint.route('/logout/')
def logout():
    """Logs a user out """
    logout_user()

    response = jsonify({
        'success': 'You have successfully logged out'
    })
    response.status_code = 200
    return response

@api_blueprint.route('/register/', methods=['POST'])
def register():
    """Registers a user

    Args:
        username (str): The user's username
        email (str): The user's email address - must follow email convention
        password (str): The user's non-hashed password

    Returns:
        201 - {'id': '<user.id>', 'username': <user.username>, 'email': <user.email>, 'so_pending': (bool)} if successful
        400 - {'error_field': ['field error1', 'field error2'...]..., } if form errors

        `so_pending` designates if the user has a pending so
    """
    
    form = RegistrationForm(data=request.get_json())
    if form.validate():
        user_created, user = User.register_user(form)
        so_pending_id = ''
        if not user_created:
            so_pending_id = User.query.filter_by(so_id=user.id).first().id
        response = jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'so_pending_id': so_pending_id,
            'created': user_created,
        })
        response.status_code = 201
        return response
    response = jsonify(form.errors)
    response.status_code = 400
    return response


@login_required
@api_blueprint.route('/update_so/', methods=['POST'])
def update_so():
    """Updates a user's Significant Other

    Searches for the significant others' username or email in the system. If
    neither are found but the email is valid, generates a new user with the
    given email and sets them as the SO of the requesting user. Otherwise sets
    the found User as this user's SO

    Args:
        username (str): The significant other's username (not required)
        email (str): The significant other's email (not required)

    Returns:
        200 - {'id': '<user.id>', 'so_id': '<user.id>'} if successful
        400 - {'error_field': ['field error1', 'field error2'...]..., } if validation errors

    Notes:
        User must be logged in to make this request
    """
    form = SOForm(data=request.get_json())
    if form.validate():
        current_user.update_so(form)

        response = jsonify({
            'id': current_user.id,
            'so_id': current_user.so_id,
            'is_so_temp': db.session.query(User).options(load_only('is_temp')).get(current_user.so_id).is_temp
        })
        response.status_code = 200
        return response
    response = jsonify(form.errors)
    response.status_code = 400
    return response

@login_required
@api_blueprint.route('/ping/', methods=['POST'])
def ping():
    """Pings the logged in user's SO

    Creates a Ping message between the user and their current SO IF the user
    has an active significant other in the system,

    Returns:
        200 - {'message_sent_at': '<datetime>'} - success
        400 - {'failure': 'You must have a significant other in the system'} - failure

    Notes:
        User must be logged in to make this request
    """
    user = User.query.get(current_user.id)
    if not user.has_so():
        response = jsonify({
            'failure': 'You must have a significant other in the system'
        })
        response.status_code = 400
        return response
    msg = user.ping_so()
    response = jsonify({
        'message_sent_at': msg.datetime,
    })
    response.status_code = 200
    return response

@login_required
@api_blueprint.route('/get_messages/', methods=['GET'])
def get_messages():
    """Gets all messages sent to current user from their current SO

    Returns:
        200 - [{'id': '<msg.id>', 'sent_at': '<msg.datetime>'}, ...] - success

    Notes:
        User must be logged in to make this request
    """
    user = User.query.get(current_user.id)
    received_messages = user.received_messages()
    response = jsonify([msg.serialize() for msg in received_messages])
    response.status_code = 200
    return response

app.register_blueprint(api_blueprint)
