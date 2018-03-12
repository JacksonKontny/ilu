# project/api/views.py
import uuid
from flask import render_template, Blueprint, request, redirect, url_for, abort, jsonify, g
from flask_login import current_user, login_required, login_user, logout_user
from flask_restful import abort

from project import db, auth, auth_token, app
from project.api.forms import RegistrationForm, SOForm, LoginForm
from project.models import User


api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/login/', methods=['POST'])
def login():
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
    logout_user()

    response = jsonify({
        'success': 'You have successfully logged out'
    })
    response.status_code = 200
    return response

@api_blueprint.route('/register/', methods=['POST'])
def register():
    form = RegistrationForm(data=request.get_json())
    if form.validate():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.save(form.password.data)
        response = jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
        })
        response.status_code = 201
        return response
    response = jsonify(form.errors)
    response.status_code = 400
    return response


@login_required
@api_blueprint.route('/update_so/', methods=['POST'])
def update_so():
    form = SOForm(data=request.get_json())
    if form.validate():
        so = db.session.query(User).filter(
            (User.username == form.username.data) | (User.email == form.email.data)
        ).first()
        if not so:
            so = User(email=form.email.data, is_temp=True)
            so.save(password=str(uuid.uuid4()))
        current_user.so_id = so.id
        current_user.save()

        response = jsonify({
            'id': current_user.id,
            'so_id': so.id,
        })
        response.status_code = 200
        return response
    response = jsonify(form.errors)
    response.status_code = 400
    return response

@login_required
@api_blueprint.route('/ping/', methods=['POST'])
def ping():
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
    user = User.query.get(current_user.id)
    received_messages = user.received_messages()
    response = jsonify([msg.serialize() for msg in received_messages])
    response.status_code = 200
    return response

app.register_blueprint(api_blueprint)
