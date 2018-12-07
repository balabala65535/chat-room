from flask import Blueprint
from flask_restful import Api

from app.blueprint.admin import view

admin = Blueprint("admin", __name__)
admin_api = Api(admin)

admin_api.add_resource(view.BlockUserView, "/block/<int:user_id>")
