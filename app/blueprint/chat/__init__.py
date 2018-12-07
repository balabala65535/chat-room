from flask import Blueprint
from flask_restful import Api

from app.blueprint.chat import view

chat = Blueprint("chat", __name__)
chat_api = Api(chat)

chat_api.add_resource(view.HomeView, "/")
chat_api.add_resource(view.AnonymousView, "/anonymous")
chat_api.add_resource(view.GetMessagesView, "/messages")
chat_api.add_resource(view.ProfileView, "/profile")
