from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager

room = dict()
display = dict()

app = Flask(__name__)

get_dict = lambda dct, *keys: {key: dct[key] for key in keys}
app.config.from_object('config')

db = MongoEngine(app)

def register_blueprints(app):
    from app.games import games
    from app.result import result
    from app.users import users
    app.register_blueprint(users)
    app.register_blueprint(result)
    app.register_blueprint(games)

register_blueprints(app)

login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view= 'users.login'


@login_manager.user_loader
def loader_user(userid):
    return model.User.objects.with_id(userid)

from app import model
