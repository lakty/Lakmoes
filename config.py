import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')
    SQLALCHEMY_DATABASE_URI = os.environ.get('HEROKU_POSTGRESQL_MAROON_URL', 'postgres://wesdftjbljfljz'
                                                                             ':1d5b0aca62beac98834be760b12b'
                                                                             'e0951b2e42e50d34d2e98dad969804a191b8'
                                                                             '@ec2-79-125-6-250.eu-west-1.compute.amazonaws.com:5432/dsomromv0fr00')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = basedir + '/images/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
