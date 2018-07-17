from betlife_api import db


class User(db.Document):
    open_id = db.StringField(required=True, unique=True)
    is_super_user = db.BooleanField(default=False)
    cards = db.IntField(required=True)
    coins = db.IntField(required=True)
    last_modified_date = db.DateTimeField(required=True)


class UserResponse:
    def __init__(self, open_id, is_super_user, **kwargs):
        self.open_id = open_id
        self.is_super_user = is_super_user

        for k, v in kwargs.items():
            setattr(self, k, v)
