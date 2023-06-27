from flask import Flask


def create_app():
    app = Flask(__name__)

    # Import and register your routes/blueprints here
    from main import app as main_blueprint

    app.register_blueprint(main_blueprint)

    return app
