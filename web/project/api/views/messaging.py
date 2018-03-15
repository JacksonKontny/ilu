from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required

from project.models import User
from project import app


messaging_blueprint = Blueprint('messaging', __name__)


@login_required
@messaging_blueprint.route('/ping/', methods=['POST'])
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
@messaging_blueprint.route('/get_messages/', methods=['GET'])
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

app.register_blueprint(messaging_blueprint)
