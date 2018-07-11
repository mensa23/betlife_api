from datetime import datetime, timedelta

from flask import Blueprint, jsonify

match = Blueprint('match', __name__)


@match.route('/future', methods=['GET'])
def get_future_matches():
    from models.match import Match
    matches = Match.objects(match_date__gt=datetime.utcnow)
    response = []
    for m in matches:
        m.match_date += timedelta(hours=8)
        from models.odd import Odd
        odd = Odd.objects(wubai_id=m.wubai_id).get()
        from models.match import MatchResponse
        match_response = MatchResponse(m.wubai_id, m.league, m.match_date, m.home_team, m.away_team, m.rang)
        if odd.profits:
            match_response.profits = odd.profits
        response.append(match_response.__dict__)
    return jsonify(response)


@match.route('/<wubai_id>', methods=['GET'])
def get_match(wubai_id):
    from models.match import Match
    m = Match.objects(wubai_id=wubai_id).get()
    m.match_date += timedelta(hours=8)
    from models.odd import Odd
    odd = Odd.objects(wubai_id=m.wubai_id).get()
    from models.match import MatchResponse
    response = MatchResponse(m.wubai_id, m.league, m.match_date, m.home_team, m.away_team, m.rang)
    if odd.profits:
        response.profits = odd.profits
    if m.home_score:
        response.home_score = m.home_score
    if m.away_score:
        response.away_score = m.away_score
    if m.result:
        response.result = m.result
    if m.result_rang:
        response.result_rang = m.result_rang
    return jsonify(response.__dict__)
