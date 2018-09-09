DEBUG = True

SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://cmsc495admin:{os.environ["DB_PASSWORD"]}@cmsc495.ce4jv8k28ioa.us-east-2.rds.amazonaws.com/cmsc_495'
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 8

CSRF_ENABLED = True
CSRF_SESSION_KEY = os.environ['APP_SECRET']

SECRET_KEY = os.environ['APP_SECRET']