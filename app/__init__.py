from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
import os

app = Flask(__name__)
log_in = LoginManager(app)
log_in.login_view = 'login'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

uri = os.environ.get('DATABASE_URL')
if uri.startswith("postgres://") if uri else False:
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 20*1024*1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg','.png','.jpeg']

#folder = str(os.path.abspath('app'))
#if folder.startswith('/app/app') if folder else False:
#    folder = folder.replace('/app/app','/app')
app.config['UPLOAD_FOLDER'] = os.path.abspath('app') +'/static/images'


db = SQLAlchemy(app)
migrate = Migrate(app,db)
from app.models import User,Upload

#import blueprints
from app.oauth.views import login_oauth
from app.login_check import login
from app.upload import upload
from app.display import display
from app.comments import comments
from app.profile import profile
#blueprints
app.register_blueprint(login_oauth,url_prefix='/oauth_login')
app.register_blueprint(login,url_prefix='/loginsimple')
app.register_blueprint(upload,url_prefix='/upload')
app.register_blueprint(display)
app.register_blueprint(comments,url_prefix='/comments')
app.register_blueprint(profile,url_prefix='/profile')

from app import views,models





