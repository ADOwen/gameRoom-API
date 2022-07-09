# easy helper that will help us create a wrapper
from functools import wraps
from flask import request, jsonify

from app.models import User

# here we are creating @token_required decorator for protecting our API routes

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({
                'status': 'error',
                'message': 'Missing auth token. Please log in with an existing account'
            })
        user = User.query.filter_by(api_token=token).first()
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'That token does not belong to a valid user'
            })
        return func(*args, **kwargs)
    return decorated