import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')
    SQLALCHEMY_DATABASE_URI = os.environ.get('HEROKU_POSTGRESQL_MAROON_URL', "postgres://uoodtxbeaoedvj"
                                                                             ":3f2ec3f64379c27eeb5e5268c467"
                                                                             "5ad546db45f241d5708d0608719de2435f93"
                                                                             "@ec2-54-246-92-116.eu-west-1."
                                                                             "compute.amazonaws.com:5432/d1hucge89ac9qc")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = basedir + '/images/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
