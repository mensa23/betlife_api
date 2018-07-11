from betlife_api import db


class Match(db.Document):
    wubai_id = db.StringField(required=True, unique=True)
    league = db.StringField(required=True)
    match_date = db.DateTimeField(required=True)
    last_modified_date = db.DateTimeField()
    home_team = db.StringField(required=True)
    away_team = db.StringField(required=True)
    home_score = db.IntField()
    away_score = db.IntField()
    rang = db.IntField(required=True)
    result = db.IntField()
    result_rang = db.IntField()


class MatchResponse:
    def __init__(self, wubai_id, league, match_date, home_team, away_team, rang, **kwargs):
        self.wubai_id = wubai_id
        self.league = league
        self.match_date = match_date
        self.home_team = home_team
        self.away_team = away_team
        self.rang = rang

        for k, v in kwargs.items():
            setattr(self, k, v)
