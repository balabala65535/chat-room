# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask import render_template, redirect, url_for, request, Blueprint, current_app, abort
from flask_login import current_user, login_required
from flask_socketio import emit
from flask_restful import Resource

from app.common.utils import to_html, flash_errors
from app.database import db_session
from app.extension import socketio
from app.forms import ProfileForm
from app.model.models import Message, User


chat_bp = Blueprint("chat_bp", __name__)


@socketio.on('new message')
def new_message(message_body):
    html_message = to_html(message_body)
    message = Message(author=current_user._get_current_object(), body=html_message)
    db_session.add(message)
    db_session.commit()
    emit('new message',
         {'message_html': render_template('chat/_message.html', message=message),
          'message_body': html_message,
          'gravatar': current_user.gravatar,
          'nickname': current_user.nickname,
          'user_id': current_user.id},
         broadcast=True)


@socketio.on('new message', namespace='/anonymous')
def new_anonymous_message(message_body):
    html_message = to_html(message_body)
    avatar = 'https://www.gravatar.com/avatar?d=mm'
    nickname = 'Anonymous'
    emit('new message',
         {'message_html': render_template('chat/_anonymous_message.html',
                                          message=html_message,
                                          avatar=avatar,
                                          nickname=nickname),
          'message_body': html_message,
          'gravatar': avatar,
          'nickname': nickname,
          'user_id': current_user.id},
         broadcast=True, namespace='/anonymous')


@socketio.on('connect')
def connect():
    global online_users
    if current_user.is_authenticated and current_user.id not in online_users:
        online_users.append(current_user.id)
    emit('user count', {'count': len(online_users)}, broadcast=True)


@socketio.on('disconnect')
def disconnect():
    global online_users
    if current_user.is_authenticated and current_user.id in online_users:
        online_users.remove(current_user.id)
    emit('user count', {'count': len(online_users)}, broadcast=True)


class HomeView(Resource):
    def get(self):
        amount = current_app.config['CATCHAT_MESSAGE_PER_PAGE']
        messages = db_session.query(Message).order_by(Message.timestamp.asc())[-amount:]
        user_amount = db_session.query(User).count()
        return render_template('chat/home.html', messages=messages, user_amount=user_amount)
        # return render_template('chat/home.html')


class AnonymousView(Resource):
    def get(self):
        return render_template('chat/anonymous.html')


class GetMessagesView(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        # sqlachemy 好像不支持
        pagination = Message.query.order_by(Message.timestamp.desc()).paginate(
            page, per_page=current_app.config['CATCHAT_MESSAGE_PER_PAGE'])
        messages = pagination.items
        return render_template('chat/_messages.html', messages=messages[::-1])


class ProfileView(Resource):
    def get(self):
        form = ProfileForm()
        if form.validate_on_submit():
            current_user.nickname = form.nickname.data
            current_user.github = form.github.data
            current_user.website = form.website.data
            current_user.bio = form.bio.data
            db_session.commit()
            return redirect(url_for('.home'))
        flash_errors(form)
        return render_template('chat/profile.html', form=form)


@chat_bp.route('/profile/<user_id>')
def get_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('chat/_profile_card.html', user=user)


@chat_bp.route('/message/delete/<message_id>', methods=['DELETE'])
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    if current_user != message.author and not current_user.is_admin:
        abort(403)
    db_session.delete(message)
    db_session.commit()
    return '', 204
