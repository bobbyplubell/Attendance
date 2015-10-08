from flask import jsonify, request, current_app, url_for
import json

from . import api
from ..models import User
from .. import db

@api.route('/users')
def users():
    users = User.query.limit(100)
    
    jsonusers = []
    for user in users:
        jsonusers.append(user.to_json())
    
    return jsonify(users=jsonusers)
