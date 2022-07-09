from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from secrets import token_hex

db = SQLAlchemy()
# create models based off of ERD (Database Tables)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    post = db.relationship('Post',backref='author', lazy=True)
    cart_item = db.relationship('Cart',backref='author', lazy=True) 
    is_admin = db.Column(db.Boolean(), default =False)
    api_token = db.Column(db.String(32), default= None, nullable= True)
    inventory_id = db.relationship('Inventory',backref='owner', lazy=True)
    

    def __init__(self, username, email, password,is_admin=False):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.is_admin = is_admin
        self.api_token = token_hex(16)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'token': self.api_token
        }        

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    username = db.Column(db.String(150), nullable= False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)


    def __init__(self, text, username, user_id):
        self.text = text
        self.username = username
        self.user_id = user_id

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'date_created': self.date_created,
            'username': self.username,
            'author': self.user_id,
        }


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    price = db.Column(db.Float())
    image = db.Column(db.String())
    description = db.Column(db.String())
    created_on = db.Column(db.DateTime, default=datetime.now)
    cart_item = db.relationship('Cart',backref='cart_product', lazy=True)

    def __init__(self, name, price, image, description):
        self.name = name
        self.price = price
        self.image = image
        self.description = description

    def to_dict(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'price' : self.price,
            'image' : self.image,
            'description' : self.description,
            'created_on' : self.created_on,
        }

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete="CASCADE"), nullable=False)

    def __init__(self, user_id, product_id):
        self.user_id = user_id
        self.product_id = product_id

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, nullable=False)
    value= db.Column(db.Integer, nullable=False)
    item_type= db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    
    
    def __init__(self, name, value, item_type, user_id):
        self.name= name
        self.value= value
        self.item_type= item_type
        self.user_id= user_id

    def to_dict(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'value' : self.value,
            'item_type' : self.item_type,
            'user_id' : self.user_id,
        }