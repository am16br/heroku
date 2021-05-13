from flask import Blueprint,url_for,session,redirect,request
from flask_login import login_user
from authlib.integrations.flask_client import OAuth
from werkzeug.security import generate_password_hash,check_password_hash
from passgen import passgen
from app import app,User,db
import os
from dotenv import load_dotenv
load_dotenv()
login_oauth = Blueprint('login_oauth',__name__)
oauth = OAuth(app)


# login fctionality with google
google = oauth.register(
    name='google',
    client_id=os.environ.get('GOOGLE_CLIENT_ID'),
    client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
)

@login_oauth.route('/google/login')
def googlelogin():
    redirect_uri = url_for('login_oauth.googleauthorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@login_oauth.route('/google/authorize')
def googleauthorize():
    token = google.authorize_access_token()
    resp = google.get('userinfo', token=token)
    resp.raise_for_status()
    user_info = resp.json()
    # do something with the token and profile
    email = user_info['email']
    password = passgen(20)
    name = user_info['name']
    user = User.query.filter_by(email=email).first()
    if user is not None:
        login_user(user,remember=True)
    else:
        user = User(name=name, email=email, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        login_user(user,remember=True)
    return redirect(url_for('display.show_post'))
#login functionality with github

github = oauth.register(
    name='github',
    client_id= os.environ.get('GITHUB_CLIENT_ID'),
    client_secret= os.environ.get('GITHUB_CLIENT_SECRET'),
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

@login_oauth.route('/github/login')
def githublogin():
    redirect_uri = url_for('login_oauth.githubauthorize', _external=True)
    return github.authorize_redirect(redirect_uri)


@login_oauth.route('/github/authorize')
def githubauthorize():
    token = github.authorize_access_token()
    resp = github.get('user', token=token)
    resp.raise_for_status()
    user_info = resp.json()
    # do something with the token and profile
    email = user_info['email']
    password = passgen(20)
    name = user_info['name']
    user = User.query.filter_by(email=email).first()
    if user is not None:
        login_user(user,remember=True)
    else:
        user = User(name=name, email=email, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        login_user(user,remember=True)
    return redirect(url_for('display.show_post'))