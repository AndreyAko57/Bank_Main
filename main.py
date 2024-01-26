from flask import Flask
from modules.routes import app as routes_app

# Create app
app = Flask(__name__)
app.register_blueprint(routes_app)


if __name__ == '__main__':
    app.run(debug=True, port=7000)
