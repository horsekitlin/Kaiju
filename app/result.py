#-*- coding:utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, request
from flask.views import MethodView
from flask.ext.login import login_required

from model import Result

result = Blueprint('result', __name__, template_folder='templates')

class ResultListView(MethodView):
    @login_required
    def get(self, userid):

        return render_template('result.html', results = Result.objects)


result.add_url_rule('/kaiju/result/<userid>', view_func = ResultListView.as_view('list'))

