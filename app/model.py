#-*- coding:utf-8 -*-
from app import db
from flask.ext.login import UserMixin

class User(db.Document, UserMixin):
    account = db.StringField(max_length=60, required=True)
    pwd = db.StringField(max_length=60, required=True)
    name = db.StringField(max_length=60)
    #email =

    meta = {
        'collection':'users'
    }

    def _get_user(self):
        return unicode(self.id)

class Words(db.Document):
    phonetic = db.StringField(max_length=5)
    word = db.StringField(max_length=2)

    meta={
        'collection':'words'
    }

class Chat(db.Document):
    time = db.DateTimeField()
    slug = db.StringField()
    user = db.ObjectIdField()


class Gamebox(db.EmbeddedDocument):
    right = db.ListField()
    wrong = db.ListField()
    live = db.ListField()

class Result(db.Document):
    user = db.ObjectIdField()
    game = db.EmbeddedDocumentField('Gamebox')

    meta={

        'collection':'result_info'
    }
