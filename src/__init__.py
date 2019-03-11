from flask import Flask
from . import dashboard, auth, webhook, mapping


# create and configure the app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'

    app.register_blueprint(auth.app)
    app.register_blueprint(dashboard.app)
    app.register_blueprint(webhook.app)
    app.register_blueprint(mapping.app)

    app.run(host='0.0.0.0', port=8000, debug=True)
    app.run(threaded=True)
    return app