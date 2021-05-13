from flask import Blueprint

login = Blueprint('login',__name__)

from app import db
from app.login_check import views, forms
