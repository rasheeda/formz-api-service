import datetime

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://mandeeya:pass@localhost/formz'
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY='somethingsecret'
<<<<<<< HEAD
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=30)
=======
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=5)
>>>>>>> 2761bea38a3ce83198864bbc678e1e65ae19f3c4
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
