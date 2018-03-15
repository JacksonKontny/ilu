#################
#### imports ####
#################

from os.path import join, isfile

from flask import Flask, render_template, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth
from flask_mail import Mail
from flask_migrate import Migrate

from instance.config import app_config


################
#### config ####
################

def create_app():
    app = Flask(__name__, instance_relative_config=True)


app = Flask(__name__, instance_relative_config=True)

if isfile(join('instance', 'flask_full.cfg')):
    app.config.from_pyfile('flask_full.cfg')
else:
    app.config.from_pyfile('flask.cfg')

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
auth = HTTPBasicAuth()
auth_token = HTTPBasicAuth()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

from project.api.views import login_blueprint
from project.api.views import account_info_blueprint
from project.api.views import messaging_blueprint

app.register_blueprint(login_blueprint)
app.register_blueprint(account_info_blueprint)
app.register_blueprint(messaging_blueprint)
