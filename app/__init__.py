from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from geopy.geocoders import Nominatim
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
nominatim = Nominatim(user_agent="fsddsfsdffs")
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager()
login.init_app(app)
login.login_view = 'login'
from app import routes, models, forms
