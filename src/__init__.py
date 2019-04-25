from flask import Flask, session, redirect, url_for, g
from . import dashboard, auth, webhook, mapping


def auth_check():
    if session.get("login") is not True:
        return redirect(url_for('/auth.index'))
    else:
        g.auth = session.get("auth")


# create and configure the app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    app.url_map.strict_slashes = False

    mapping.app.before_request(auth_check)
    webhook.app.before_request(auth_check)

    app.register_blueprint(auth.app)
    app.register_blueprint(dashboard.app)
    app.register_blueprint(webhook.app)
    app.register_blueprint(mapping.app)

    app.run(host='0.0.0.0', port=8000, threaded=True)
    app.run(debug=True)
    return app