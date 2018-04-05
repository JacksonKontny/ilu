from flask import Blueprint, request, jsonify, url_for, redirect
from flask_login import current_user, login_user, logout_user

from project import app, db, google_blueprint
from project.api.forms.forms import LoginForm
from project.models import User, OAuth
from sqlalchemy.orm.exc import NoResultFound

from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin, SQLAlchemyBackend
from flask_dance.contrib.google import make_google_blueprint, google

login_blueprint = Blueprint('login', __name__)


@google_blueprint.route("/google_login/")
def index():
    if not current_user.is_authenticated:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    return "You are {email} on Google".format(email=resp.json()["email"])

@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(blueprint, token):
    if not token:
        # flash("Failed to log in with Google.", category="error")
        return False

    resp = blueprint.session.get("/oauth2/v2/userinfo")
    if not resp.ok:
        msg = "Failed to fetch user info from Google."
        # flash(msg, category="error")
        return False

    google_info = resp.json()
    google_user_id = str(google_info["id"])

    # Find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(
        provider=blueprint.name,
        provider_user_id=google_user_id,
    )
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(
            provider=blueprint.name,
            provider_user_id=google_user_id,
            token=token,
        )

    if oauth.user:
        login_user(oauth.user)
        # flash("Successfully signed in with google.")

    else:
        # Create a new local user account for this user
        user = User(
            # Remember that `email` can be None, if the user declines
            # to publish their email address on google!
            email=google_info["email"],
            given_name=google_info["given_name"],
            family_name=google_info["family_name"],
            picture_url=google_info["picture"],
            gender=google_info["gender"],
        )
        # Associate the new local user account with the OAuth token
        oauth.user = user
        # Save and commit our database models
        db.session.add_all([user, oauth])
        db.session.commit()
        # Log in the new local user account
        login_user(user)
        # flash("Successfully signed in with google.")

    # Disable Flask-Dance's default behavior for saving the OAuth token
    return False

# notify on OAuth provider error
@oauth_error.connect_via(google_blueprint)
def google_error(blueprint, error, error_description=None, error_uri=None):
    msg = (
        "OAuth error from {name}! "
        "error={error} description={description} uri={uri}"
    ).format(
        name=blueprint.name,
        error=error,
        description=error_description,
        uri=error_uri,
    )
    # flash(msg, category="error")

@login_blueprint.route('/login_standard/', methods=['POST'])
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
    import time
    if current_user.is_authenticated:
        logout_user()
    form = LoginForm()
    if form.validate():
        user = User.query.filter_by(email=form.email.data).one()
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
