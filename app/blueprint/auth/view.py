from flask import render_template, flash, redirect, url_for, Blueprint, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_restful import Resource

from app.database import db_session
from app.model.models import User


class LoginView(Resource):
    """
    登录
    """
    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('chat.home'))
        return render_template('auth/login.html')

    def post(self):
        email = request.form['email']
        password = request.form['password']
        remember_me = request.form.get('remember', False)

        if remember_me:
            remember_me = True

        user = User.query.filter_by(email=email).first()

        if user is not None:
            if user.password_hash is None:
                flash('Please use the third party service to log in.')
                return redirect(url_for('.login'))

            if user.verify_password(password):
                login_user(user, remember_me)
                return redirect(url_for('chat.home'))
        flash('Either the email or password was incorrect.')
        return redirect(url_for('.login'))


class LogoutView(Resource):
    """
    退出
    """
    def get(self):
        logout_user()
        return redirect(url_for('chat.home'))


class RegisterView(Resource):
    """
    注册
    """
    def get(self):
        # if current_user.is_authenticated:
        #     return redirect(url_for('main.index'))
        return render_template('auth/register.html')

    def post(self):
        email = request.form['email'].lower()

        user = User.query.filter_by(email=email).first()
        if user is not None:
            flash('The email is already registered, please log in.')
            return redirect(url_for('.login'))

        nickname = request.form['nickname']
        password = request.form['password']

        user = User(nickname=nickname, email=email)
        user.set_password(password)
        db_session.add(user)
        db_session.commit()
        login_user(user, remember=True)
        return redirect(url_for('chat.profile'))


