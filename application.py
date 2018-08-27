from flask import Flask

application = Flask(__name__)


@application.route("/")
def welcome():
    return "Hello World! This is a Flask application for CMSC495-6381."


if __name__ == "__main__":
    application.run()
