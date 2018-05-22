import flask.ext.login as flask_login
from flask import current_app, g, Blueprint, jsonify, abort
from flask.ext.login import login_required

users_blueprint = Blueprint('users', __name__)

class User(flask_login.UserMixin):
    def __init__(self, id, name, email, mbti):
        self.id = id
        self.name = name
        self.email = email
        self.mbti = mbti

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'mbti': self.mbti,
            # required by Ember
            'type': 'user'
        }

# get a user by their user id
def get_user_by_user_id(id, cursor):
    cursor.execute('SELECT name, email, mbti FROM users WHERE id=%s', id)
    result = cursor.fetchone()
    if result == None:
        return None
    else:
        user = User(id, result[0], result[1], result[2])
        return user

# get a user by their email and password
def get_user_by_credentials(email, password, cursor):
    cursor.execute('SELECT id FROM users WHERE email=%s AND password=%s', (email, password))
    result = cursor.fetchone()
    if result == None:
        return None
    else:
        return get_user_by_user_id(result[0], cursor)

# get a user by their email address
def get_user_by_email(email, cursor):
    cursor.execute('SELECT id FROM users WHERE email=%s', email)
    result = cursor.fetchone()
    if result == None:
        return None
    else:
        return get_user_by_user_id(result[0], cursor)

# create a new user in the database
def create_user(name, email, mbti, password, cursor):
    # check for existing user
    if get_user_by_email(email, cursor) is not None:
        # instead of returning None when the user already exists, it would
        # probably be cleaner to raise an Error with Python's "raise" and
        # then surround the call to this function in "try" and "except".
        # Really that goes for all of the server code, I haven't been using
        # raise at all, usually I just return None if there was an issue
        return None
    else:
        cursor.execute('INSERT INTO users VALUES (0, %s, %s, %s, %s)', (name, email, mbti, password))
        return get_user_by_email(email, cursor)

@users_blueprint.route('/users/<int:id>')
@login_required
def get_user_by_user_id_route(id):
    user = get_user_by_user_id(id, g.db.cursor())
    if user == None:
        # HTTP 400 means Bad Request
        abort(400)
    else:
        return jsonify(user=user.serialize())
