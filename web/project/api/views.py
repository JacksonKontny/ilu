# project/api/views.py
import uuid
from flask import render_template, Blueprint, request, redirect, url_for, abort, jsonify, g
from flask.ext.restful import abort
from flask_login import current_user, login_required

from project import db, auth, auth_token, app
from project.web.forms import RegistrationForm, SOForm
from project.models import User


api_blueprint = Blueprint('api', __name__)


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
            'user_id': user.user_id,
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
            so.save(password=uuid.uuid())
        current_user.so_id = so.user_id
        current_user.save()

        response = jsonify({
            'user_id': current_user.user_id,
            'so_id': so.user_id,
        })
        response.status_code = 201
        return response
    response = jsonify(form.errors)
    response.status_code = 400
    return response


app.register_blueprint(api_blueprint)
