import os

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://root@localhost/cmsc_495'
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 8

CSRF_ENABLED = True
CSRF_SESSION_KEY = "secret"
SECRET_KEY = os.environ['APP_SECRET']
STRIPE_SECRET_KEY = os.environ['STRIPE_SECRET_KEY']
STRIPE_WH_SECRET = os.environ['STRIPE_WH_SECRET']
S3_INVENTORY_BUCKET = 'teamflaskapp-inventory-images'