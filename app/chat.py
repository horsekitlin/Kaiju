#-*- coding:utf-8 -*-
from flask import Blueprint, redirect, render_template
from flask.views import MethodView
from flask.ext.login import login_required
from model import Words
from random import randint
from app import app

chat = Blueprint('chat', __name__, template_folder='templates')

class ChatListView(MethodView):
    @login_required
    def get(self, userid):
        return render_template('chatlist.html')


chat_view = ChatView.as_view('games')
chat.add_url_rule('/chat/<userid>', defaults={'userid':None},
        view_func = chat_view, methods=['GET'])
