#-*- coding:utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, request
from flask.views import MethodView
from flask.ext.login import (login_user, logout_user, login_required,
        current_user)

from model import User
from forms import LoginForm, AddUserForm
from app import get_dict
users = Blueprint('users', __name__, template_folder='templates')



class LoginView(MethodView):
    def get(self):
        if current_user.is_authenticated():
            return render_template('index.html', users=User.objects)#登入
        else:
            form = LoginForm()
            return render_template('login.html', form=form)

    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            user = form._get_user()
            login_user(user)
            return render_template('index.html')
        return render_template('login.html', form=form)

class LogoutView(MethodView):

    @login_required
    def get(self):
        logout_user()
        return redirect(url_for('users.login'))

class AddUserView(MethodView):
    def get(self):
        form = AddUserForm()
        return render_template('create.html', form=form)
    def post(self):
        user_dict = get_dict(request.form, u'account', u'pwd', u'name')
        u = User(**user_dict)
        u.save()
        return redirect(url_for('users.login'))

users.add_url_rule('/', view_func = LoginView.as_view('login'))
users.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
users.add_url_rule('/adduser', view_func=AddUserView.as_view('adduser'))

