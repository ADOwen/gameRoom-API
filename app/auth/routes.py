from flask import Blueprint,request, jsonify
from werkzeug.security import check_password_hash

from app.models import User

auth = Blueprint('auth',__name__)

from app.models import db

@auth.route('/api/login', methods=['POST'])
def apiLogin():
    data = request.json
    print(data)

    username = data['username']
    password = data['password']


    user = User.query.filter_by(username=username).first()

    if user is None or not check_password_hash(user.password, password):
        return jsonify({
                'status': 'error',
                'message': 'Incorrect username or password'
            })
    return jsonify({
        'status' : 'success',
        'message': f'Welcome back, {username}',
        'data': user.to_dict(),
        'token' : user.api_token
    })



@auth.route('/api/register', methods=['POST'])
def apiRegister():
    # grabbing the body of the json body from the request
    data = request.json
    print(data)

    username = data['username']
    email = data['email']
    password = data['password']
    confirm_password = data['confirmPassword']

    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({
                'status': 'error',
                'message': 'User with that username already exists'
            })
    
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({
                'status': 'error',
                'message': 'User with that email already exists'
            })

    if password == confirm_password:
        user = User(username, email, password)
        
        db.session.add(user)
        db.session.commit()
        return jsonify({
                'status' : 'success',
                'data': user.to_dict(),
                'message': f"Account succesfully created for {username}",
            })

    return { 'status' : 'error', 'message' : 'Passwords do not match' }