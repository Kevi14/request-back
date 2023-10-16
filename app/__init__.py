import os
import logging
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.middlewares.standardize_response import standardize_response

# Set up logging configuration
logging.basicConfig(filename='application.log', level=logging.INFO,
                    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)
config_file = os.environ.get('FLASK_CONFIG', 'config')
app.config.from_object(config_file)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.middlewares.error_handler import handle_error
from app.routes import api,get_http_request

if __name__ == '__main__':
    app.run()
