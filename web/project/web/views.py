# project/recipes/views.py

#################
#### imports ####
#################

from flask import render_template, Blueprint, request, redirect, url_for, flash, abort, jsonify
from flask_login import current_user, login_required
from project import app, db
from project.models import *
from random import random


################
#### config ####
################

view_blueprint = Blueprint('view', __name__)


##########################
#### helper functions ####
##########################

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'info')
################
#### routes ####
################

@view_blueprint.route('/')
def hello_world():
    return 'Hello World'

app.register_blueprint(view_blueprint)
