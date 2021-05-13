from flask import Blueprint

display = Blueprint('display',__name__)

from app.display import routes