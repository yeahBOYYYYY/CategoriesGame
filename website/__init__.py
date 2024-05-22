from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "$a$dasHdfSfA118917^234@2%"

    return app