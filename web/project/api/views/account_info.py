from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required

from sqlalchemy.orm import load_only

from project import db
from project.api.forms.forms import RegistrationForm, SOForm
from project.models import User


account_info_blueprint = Blueprint('account_info', __name__)


@account_info_blueprint.route('/register/', methods=['POST'])
def register():
    """Registers a user if they do not wish to use OAuth

    Args:
        email (str): The user's email address - must follow email convention
        password (str): The user's non-hashed password

    Returns:
        201 - {'id': '<user.id>', 'email': <user.email>, 'so_pending': (bool)} if successful
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
@account_info_blueprint.route('/update_so/', methods=['POST'])
def update_so():
    """Updates a user's Significant Other

    Searches for the significant others' username or email in the system. If
    neither are found but the email is valid, generates a new user with the
    given email and sets them as the SO of the requesting user. Otherwise sets
    the found User as this user's SO

    Args:
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
