from flask import Blueprint
from flask_restful import Api

from app.blueprint.auth import view

auth = Blueprint("auth", __name__)
auth_api = Api(auth)

auth_api.add_resource(view.LoginView, "/login")
auth_api.add_resource(view.LogoutView, "/logout")
auth_api.add_resource(view.RegisterView, "/register")
