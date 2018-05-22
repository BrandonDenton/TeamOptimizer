from flask import Flask, request, jsonify, abort, redirect, url_for, g
import flask.ext.login as flask_login
from flask.ext.login import login_required
import pymysql, config
from groups import groups_blueprint
from auth import auth_blueprint
from users import users_blueprint, get_user_by_user_id

app = Flask(__name__)
app.debug = True # TODO: change in production
app.secret_key = '1337'

app.register_blueprint(groups_blueprint, url_prefix='/api')
app.register_blueprint(auth_blueprint, url_prefix='/api')
app.register_blueprint(users_blueprint, url_prefix='/api')

@app.before_request
def before_request():
    g.db = pymysql.connect(config.SQL_HOSTNAME, config.SQL_USERNAME, config.SQL_PASSWORD, config.SQL_DATABASE_NAME)

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.commit()
        db.close()

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(id):
    return get_user_by_user_id(id, g.db.cursor())

@login_manager.unauthorized_handler
def unauthorized_handler():
    abort(401)

if __name__ == '__main__':
    app.run()
