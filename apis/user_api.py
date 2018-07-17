from datetime import datetime

import requests
from flask import Blueprint, request, jsonify

from settings import MP_APP_ID, MP_APP_SECRET

user = Blueprint('user', __name__)

super_open_ids = ['oKBQB5cR8MLzO7PvJOoLDCGr4BWc']


@user.route('/login', methods=['POST'])
def login():
    payload = request.json
    code = payload['code']
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % (
        MP_APP_ID, MP_APP_SECRET, code)
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url=url, headers=headers).json()
    open_id = response['openid']
    from models.user import User
    u = User.objects(open_id=open_id).first()
    if not u:
        u = User(open_id=open_id, cards=10, coins=100)
        if open_id in super_open_ids:
            u.is_super_user = True
    u.last_modified_date = datetime.utcnow()
    u = u.save()
    from models.user import UserResponse
    user_response = UserResponse(open_id, u.is_super_user)
    return jsonify(user_response.__dict__)
