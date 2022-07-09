from flask import Blueprint, jsonify, request

from app.api_auth_helper import token_required
from ..models import  Post, User


blog = Blueprint('blog', __name__)

from app.models import db

@blog.route('/api/posts')
def apiPosts():
    posts = Post.query.all()
    
    return jsonify([post.to_dict() for post in posts])

@blog.route('/api/create/post', methods=['POST'])
def apiRegister():
    # grabbing the body of the json body from the request
    data = request.json
    print(data)

    username = data['username']
    id = data['id']
    text = data['text']

    user = User.query.filter_by(username=username).first()
    if user:
        post = Post(text,username, id)
        
        db.session.add(post)
        db.session.commit()
        
        return jsonify({
                'status': 'success',
                'message': f'User {username} has succesfully created a post'
            })
    
    return { 'status' : 'error', 'message' : 'Must have a valid username to create a post' }