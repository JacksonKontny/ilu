#################
#### imports ####
#################

from os.path import join, isfile

from flask import Flask, render_template, make_response, jsonify, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
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

config = configparser.ConfigParer()
config.read('oauth.ini')
GOOGLE_OAUTH_CLIENT_ID = config['google']['client_id']
GOOGLE_OAUTH_SECRET = config['google']['client_secret']
google_blueprint = make_google_blueprint(
    client_id=GOOGLE_OAUTH_CLIENT_ID,
    client_secret=GOOGLE_OAUTH_SECRET,
    scope=["profile", "email"]
)

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
auth = HTTPBasicAuth()
auth_token = HTTPBasicAuth()

login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_view = "google.login"
login_manager.login_view = "users.login"

from project.api.views import login_blueprint
from project.api.views import account_info_blueprint
from project.api.views import messaging_blueprint

app.register_blueprint(login_blueprint)
app.register_blueprint(account_info_blueprint)
app.register_blueprint(messaging_blueprint)

from project.models import OAuth
from flask_login import current_user
google_blueprint.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)

app.register_blueprint(google_blueprint)
