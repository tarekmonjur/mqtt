from flask import Flask
from . import dashboard, auth
# from db import db
import db as db


# create and configure the app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'

    app.register_blueprint(dashboard.app)
    app.register_blueprint(auth.app)

    app.run(host='0.0.0.0', port=8000, debug=True)
    app.run(threaded=True)
    return app