#-*- coding:utf-8 -*-
from flask import Blueprint, redirect, render_template, jsonify
from flask.views import MethodView
from flask.ext.login import login_required
from bson.objectid import ObjectId
from json import dumps, loads
from model import Words, Result, User
from random import randint
from app import app, room, display, get_dict

games = Blueprint('game', __name__, template_folder='templates')

"""
room ={
    "user":["userid"],
    "userid":{
        "right":[],
        "wrong":[],
        "live":[]
    }
}
"""

class WordGames(MethodView):
    def random_index(self):
        index_arr = ["a", "b", "c", "d", "e"]
        return index_arr[randint(0,4)]

    @login_required
    def get(self, userid):
        user = User.objects.with_id(userid)
        room["game"]={
            "user": ObjectId(userid),
            "status":'live',
            "game":{
                "live":list(),
                "right" : list(),
                "wrong" : list(),
                "dead" : list()
            }
        }

        display["game"] = dict({
            "a" : list(['']*5),
            "b" : list(['']*5),
            "c" : list(['']*5),
            "d" : list(['']*5),
            "e" : list(['']*5)
        })
        return render_template('game.html',
                display=display["game"],
                u = user,
                chat_ip = app.config["CHATROOM"])
    def post(self, userid):
        for index in ["a","b","c","d","e"]:
            if '' not in display[userid][index]:
                game_result = Result(**room[userid])
                game_result.save()
                return 'dead'
            for num in [4,3,2,1,0]:
                if num == 4:
                    continue
                if display[userid][index][num+1] != '':
                    continue
                if display[userid][index][num] is not '':
                    display[userid][index][num+1] = display[userid][index][num]
                    display[userid][index][num]=''
        return dumps(display[userid])

    def put(self, userid):
        word = Words.objects[randint(0,Words.objects.count())]
        game = room[userid]["game"]
        game["live"].append(word["word"])
        #w = get_dict(word, 'word', 'phonetic')
        index = self.random_index()
        display[userid][index][0] = word["word"]
        result = dumps(display[userid])
        return result

    def delete(self, userid, word):
        delete = dict()
        delete["word"] = word
        delete['userid'] = userid
        live = room[userid]['game']['live']
        if word in room[userid]["game"]['live']:
            for index in ["a", "b", "c", "d", "e"]:
                for num in [4,3,2,1,0]:
                    if display[userid][index][num] == word:
                        display[userid][index][num]=''

            room[userid]['game']['live'] = [ w for w in live if w != word ]
            room[userid]['game']['right'].append(w)
            delete['check'] = 'right'
        else:
            room[userid]['game']['wrong'].append(w)
            delete['check'] = 'wrong'

        return dumps(delete)

games_view = WordGames.as_view('games')
games.add_url_rule('/kaiju/game/<userid>',
                view_func = games_view, methods=['GET'])
games.add_url_rule('/kaiju/game/put/<userid>', view_func=games_view, methods=['PUT'])
games.add_url_rule('/kaiju/game/post/<userid>', view_func=games_view, methods=['POST'])
games.add_url_rule('/kaiju/game/del/<userid>/<word>', view_func=games_view, methods=['DELETE'])
