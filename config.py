import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://myuser:mypassword@db/mydatabase'