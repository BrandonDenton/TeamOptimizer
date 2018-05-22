import flask.ext.login as flask_login
from flask.ext.login import login_required
from users import get_user_by_credentials, create_user
from flask import abort, g, request, jsonify, Blueprint, current_app

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    user = get_user_by_credentials(email, password, g.db.cursor())

    if user == None:
        abort(401)
    else:
        flask_login.login_user(user)
        current_app.logger.info('{} logged in'.format(email))
        return jsonify(user.serialize())

@auth_blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    email = flask_login.current_user.email
    flask_login.logout_user()
    current_app.logger.info('{} logged out'.format(email))
    return jsonify(message='Successfully logged out')

# our authentication on the client is mostly done by extending ember-simple-auth's
# BaseAuthenticator class (in client/authenticators/teamop-auth.js). BaseAuthenticator
# has a virtual method called restore() that is used by ember-simple-auth to determine
# if the user is logged in after a page refresh. we have implemented this method on
# the client to simply make an AJAX call to this /restore route -- if the user is not
# logged in, a 401 Not Authorized will be returned from this route and the user will
# not be authenticated on the client. if the user is logged in, this route returns
# the currently logged in user object, and ember-simple-auth saves it.
# here's the ember-simple-auth documentation on restore():
# http://ember-simple-auth.com/api/classes/BaseAuthenticator.html
@auth_blueprint.route('/restore')
@login_required
def restore():
    user = flask_login.current_user
    return jsonify(user.serialize())

@auth_blueprint.route('/register', methods=['POST'])
def register():
    name = request.form['fullName']
    email = request.form['email']
    mbti = request.form['mbti'].lower() # ensure it's lowercase
    password = request.form['password']

    # probably should be using try / except here instead of checking
    # if the return value is None
    user = create_user(name, email, mbti, password, g.db.cursor())
    if user == None:
        abort(400)
    else:
        return jsonify(user.serialize())
