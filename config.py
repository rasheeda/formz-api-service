import datetime

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://mandeeya:pass@localhost/formz'
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY='somethingsecret'
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=5)
