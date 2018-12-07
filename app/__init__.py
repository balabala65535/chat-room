# -*- coding = utf-8 -*-
from __future__ import absolute_import
import datetime
import time
from decimal import Decimal

from flask import Flask
from flask.json import JSONEncoder
from flask_login import AnonymousUserMixin

from app.config import Config
from app.extension import login_manager


def create_app():
    application = Flask("chat_rom",
                        static_folder="static", template_folder="templates")
    application.config.from_object(Config)
    config_app(application)
    config_extension(application)
    config_blueprint(application)

    return application


def config_app(app):
    """

    :type app: Flask
    """

    class CustomJSONEncoder(JSONEncoder):
        """自定义返回参数的处理"""

        def default(self, o):

            # 对于时间类型返回毫秒级整型
            if isinstance(o, datetime.datetime):
                return int(time.mktime(o.timetuple()) * 1000)
            if isinstance(o, Decimal):
                return float("%.3f" % o)
            if o is None:
                return 0

            return super(CustomJSONEncoder, self).default(o)

    app.json_encoder = CustomJSONEncoder

    app.secret_key = "nlm23nkjmkn123jk4hui9"


def config_extension(app):
    @login_manager.user_loader
    def load_user(user_id):
        from app.database import db_session
        from app.model.models import User

        user = db_session.query(User).get(user_id)
        if not user:
            return AnonymousUserMixin()
        return user


def config_blueprint(app):
    """

    :type app: Flask
    """
    pass

    from app.blueprint.admin import admin
    app.register_blueprint(admin)
    from app.blueprint.auth import auth
    app.register_blueprint(auth)
    from app.blueprint.chat import chat
    app.register_blueprint(chat)
    from app.blueprint.chat.view import chat_bp
    app.register_blueprint(chat_bp)
    from app.blueprint.oauth import oauth
    app.register_blueprint(oauth)


