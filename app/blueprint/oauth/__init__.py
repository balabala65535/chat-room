from flask import Blueprint
from flask_restful import Api

from app.blueprint.chat import view

oauth = Blueprint('oauth', __name__)