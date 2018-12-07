# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import hashlib
from datetime import datetime

from flask import current_app
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, AnonymousUserMixin
from sqlalchemy import (Column, Integer, String, DateTime, Text, ForeignKey)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

from app import login_manager

Base = declarative_base()
bcrypt = Bcrypt()


class User(UserMixin, Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    access_token = Column(String(128))
    email = Column(String(254), unique=True, nullable=False)
    nickname = Column(String(30))
    password_hash = Column(String(128))
    email_hash = Column(String(128))
    github = Column(String(255))
    website = Column(String(255))
    bio = Column(String(120))
    messages = relationship('Message', back_populates='author', cascade='all')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.generate_email_hash()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_email_hash(self):
        if self.email is not None and self.email_hash is None:
            self.email_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()  # encode for py23 compatible

    @property
    def is_admin(self):
        return self.email == current_app.config['CATCHAT_ADMIN_EMAIL']

    @property
    def gravatar(self):
        return 'https://gravatar.com/avatar/%s?d=monsterid' % self.email_hash


class Guest(AnonymousUserMixin):

    @property
    def is_admin(self):
        return False


login_manager.anonymous_user = Guest


class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True)
    body = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    author_id = Column(Integer, ForeignKey('user.id'))
    author = relationship('User', back_populates='messages')
