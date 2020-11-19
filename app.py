from flask import Flask
from flasgger import Swagger
from routes.home import home
from flask_cors import CORS


def create_app():
  app = Flask(__name__)

  app.register_blueprint(home, url_prefix='/home')

  cors = CORS(app, resources={r"/*": {"origins": "*"}})

  return app

if __name__ == "__main__":
  from argparse import ArgumentParser

  parser = ArgumentParser()
  parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
  args = parser.parse_args()

  app = create_app()
  app.run(debug=True, host='0.0.0.0', port=args.port)