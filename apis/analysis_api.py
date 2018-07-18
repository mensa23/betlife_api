from datetime import datetime, timedelta

from flask import Blueprint, jsonify

analysis = Blueprint('analysis', __name__)


@analysis.route('/profit/<wubai_id>', methods=['GET'])
def get_profit(wubai_id):
    from models.odd import Odd
    o = Odd.objects(wubai_id=wubai_id).first()
    probabilities = [round(o.sp_home * 100, 1), round(o.sp_draw * 100, 1), round(o.sp_away * 100, 1)]
    from models.profit import ProfitResponse
    response = ProfitResponse(probabilities, [])
    if o.profits:
        size = len(o.profits)
        total_init_profit_home = 0
        total_init_profit_draw = 0
        total_init_profit_away = 0
        total_new_profit_home = 0
        total_new_profit_draw = 0
        total_new_profit_away = 0
        for p in o.profits:
            total_init_profit_home += p['init_sp_profit']['init_profit_home']
            total_init_profit_draw += p['init_sp_profit']['init_profit_draw']
            total_init_profit_away += p['init_sp_profit']['init_profit_away']
            total_new_profit_home += p['new_sp_profit']['new_profit_home']
            total_new_profit_draw += p['new_sp_profit']['new_profit_draw']
            total_new_profit_away += p['new_sp_profit']['new_profit_away']
        profits = [round(total_init_profit_home / size, 3), round(total_init_profit_draw / size, 3),
                   round(total_init_profit_away / size, 3), round(total_new_profit_home / size, 3),
                   round(total_new_profit_draw / size, 3), round(total_new_profit_away / size, 3)]
        response.profits = profits
    return jsonify(response.__dict__)


@analysis.route('/accuracy/<int:hours>', methods=['GET'])
def get_accuracy(hours):
    now = datetime.utcnow()
    from models.match import Match
    matches = Match.objects(match_date__lt=now, match_date__gte=now - timedelta(hours=hours), result__exists=True)
    bingo = 0
    for m in matches:
        wubai_id = m.wubai_id
        from models.odd import Odd
        o = Odd.objects(wubai_id=wubai_id).first()
        if o.profits:
            size = len(o.profits)
            total_init_profit_home = 0
            total_init_profit_draw = 0
            total_init_profit_away = 0
            total_new_profit_home = 0
            total_new_profit_draw = 0
            total_new_profit_away = 0
            for p in o.profits:
                total_init_profit_home += p['init_sp_profit']['init_profit_home']
                total_init_profit_draw += p['init_sp_profit']['init_profit_draw']
                total_init_profit_away += p['init_sp_profit']['init_profit_away']
                total_new_profit_home += p['new_sp_profit']['new_profit_home']
                total_new_profit_draw += p['new_sp_profit']['new_profit_draw']
                total_new_profit_away += p['new_sp_profit']['new_profit_away']
            profits = [round(total_init_profit_home / size, 3), round(total_init_profit_draw / size, 3),
                       round(total_init_profit_away / size, 3), round(total_new_profit_home / size, 3),
                       round(total_new_profit_draw / size, 3), round(total_new_profit_away / size, 3)]
            results = [3, 1, 0]
            if profits[3] < 0:
                results.remove(3)
            if profits[4] < 0:
                results.remove(1)
            if profits[5] < 0:
                results.remove(0)
            if m.result_rang in results:
                bingo += 1
    response = {'bingo': round(bingo / matches.count() * 100, 1)}
    return jsonify(response)
