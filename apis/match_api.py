from datetime import datetime, timedelta

from flask import Blueprint, jsonify

match = Blueprint('match', __name__)


@match.route('/future/<int:hours>', methods=['GET'])
def get_future_matches(hours):
    now = datetime.utcnow()
    from models.match import Match
    matches = Match.objects(match_date__gt=now, match_date__lte=now + timedelta(hours=hours)).order_by('match_date')
    response = []
    for m in matches:
        match_date = m.match_date + timedelta(hours=8)
        match_date_str = datetime.strftime(match_date, '%Y-%m-%d %H:%M:%S')
        from models.match import MatchResponse
        match_response = MatchResponse(m.wubai_id, m.league, match_date_str, m.home_team, m.away_team, m.rang)
        response.append(match_response.__dict__)
    return jsonify(response)


@match.route('/<wubai_id>', methods=['GET'])
def get_match(wubai_id):
    from models.match import Match
    m = Match.objects(wubai_id=wubai_id).first()
    match_date = m.match_date + timedelta(hours=8)
    match_date_str = datetime.strftime(match_date, '%Y-%m-%d %H:%M:%S')
    from models.match import MatchResponse
    response = MatchResponse(m.wubai_id, m.league, match_date_str, m.home_team, m.away_team, m.rang)
    if hasattr(m, 'home_score'):
        response.home_score = m.home_score
    if hasattr(m, 'away_score'):
        response.away_score = m.away_score
    if hasattr(m, 'result'):
        response.result = m.result
    if hasattr(m, 'result_rang'):
        response.result_rang = m.result_rang
    return jsonify(response.__dict__)
