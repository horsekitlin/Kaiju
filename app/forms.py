#-*- coding:utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required, ValidationError
from model import User
class AddUserForm(Form):
    account=TextField(u'帳號', validators=[Required(message=u'帳號請勿空白')])
    pwd = TextField(u'密碼', validators=[Required(message=u'密碼請勿空白')])
    name = TextField(u'暱稱')
    def validate_account(self, field):
        if User.objects(account=self.account.data).count() > 0:
            raise ValidationError(u'此帳號已存在！')

    def validate_pwd(self, field):
        if len(field.data) < 5:
            raise ValidationError(u'密碼請大於5個字元！')

class LoginForm(Form):
    account = TextField(u'帳號', validators=[Required(message=u"帳號請勿空白")])
    pwd = PasswordField(u'密碼', validators=[Required(message=u"密碼請勿空白")])

    def _get_user(self):
        try:
            user = User.objects(account = self.account.data).first()

        except MultipleObjectsReturned:#若搜尋到兩個以上的使用者，則抓取第一個
            user = user[0]
        return user

    def validate_account(self, field):
        if self._get_user() is None:
            raise ValidationError(u'該使用者不存在！')

    def validate_pwd(self, field):
        user = self._get_user()
        if user and user.pwd != field.data:
            raise ValidationError(u"密碼不正確")
