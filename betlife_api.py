from flask import Flask
from flask_mongoengine import MongoEngine

from apis.match_api import match
from settings import DATABASE_NAME

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': DATABASE_NAME
}
app.config['JSON_AS_ASCII'] = False

app.register_blueprint(match, url_prefix='/api/matches')

db = MongoEngine(app)

if __name__ == '__main__':
    app.run()
