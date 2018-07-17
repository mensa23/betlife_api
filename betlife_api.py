from flask import Flask
from flask_mongoengine import MongoEngine

from apis.match_api import match
from apis.profits_api import profit
from apis.user_api import user
from settings import DATABASE_NAME

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': DATABASE_NAME
}
app.config['JSON_AS_ASCII'] = False

app.register_blueprint(match, url_prefix='/api/matches')
app.register_blueprint(user, url_prefix='/api/users')
app.register_blueprint(profit, url_prefix='/api/profits')

db = MongoEngine(app)

if __name__ == '__main__':
    app.run()
