from betlife_api import db


class Odd(db.Document):
    wubai_id = db.StringField(required=True, unique=True)
    last_modified_date = db.DateTimeField()
    rang = db.IntField(required=True)
    sp_home = db.FloatField(required=True)
    sp_draw = db.FloatField(required=True)
    sp_away = db.FloatField(required=True)
    odds = db.ListField(db.DictField())
    rangs = db.ListField(db.DictField())
    profits = db.ListField(db.DictField())
