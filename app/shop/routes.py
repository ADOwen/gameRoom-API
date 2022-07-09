from flask import Blueprint, redirect, jsonify, request
from app.api_auth_helper import token_required
from app.models import Cart, Product, User, Inventory

import os
import stripe

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

# create instance of blueprint
shop = Blueprint('shop', __name__)

from app.models import db

@shop.route('/api/shop/products')
def allProductsAPI():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])


@shop.route('/api/shop/<int:id>')
def individualProductAPI(id):
    product = Product.query.filter_by(id=id).first()
    if product is None:
        return jsonify('none')
    return jsonify(product.to_dict())

@shop.route('/stripe/createCheckoutSession', methods=['POST'])
def createStripeCheckout():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                "price": 'price_1KM2gAKlKs2BiYWweBJIloCY',
                "quantity": 1
            }],
            mode='payment',
            success_url = 'http://localhost:3000/',
            cancel_url = 'http://localhost:3000/cart',
        )

    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

@shop.route('/api/getCart', methods=['POST'])
def getCart():
    data = request.json
    user_id = data['user_id']
    cart = Cart.query.filter_by(user_id = user_id)
    return jsonify([Product.query.filter_by(id=instance.product_id).first().to_dict() for instance in cart])
    

@shop.route('/api/addToCart', methods=['POST'])
def addToCart():
    data = request.json
    print(data)
    user_id = data['user_id']
    product_id = data['product_id']
    
    newCartItem = Cart(user_id, product_id)
    db.session.add(newCartItem)
    db.session.commit()

    return jsonify({
        'status': 'succes',
        'message': f'You have succesfully added item {product_id} to your cart'
    })

@shop.route('/api/removeFromCart', methods=['POST'])
def deleteCartItem():
    data = request.json
    print(data)
    user_id = data['user_id']
    product_id= data['product_id']
    print(user_id)
    # user = User.query.filter_by(id= user_id)

    cart_item= Cart.query.filter_by(user_id = user_id).filter_by(product_id= product_id).first()
    print(cart_item)
          
    
    db.session.delete(cart_item)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': f'item has been removed'
    })


@shop.route('/api/inventory', methods=['POST'])
def updateInventory():
    data= request.json
    
    user_id = data['user_id']   
    item_name = data['item_name']
    value = data['value']
    item_type = data['item_type']

    user = User.query.filter_by(id=user_id).first()
    if user:
        newInventoryitem = Inventory(item_name, value, item_type, user_id)
        db.session.add(newInventoryitem)
        db.session.commit()
       
        
        return jsonify({
        'status': 'succes',
        'message': f'You have succesfully added item {item_name} to your cart'
    })

    return jsonify({
        'status': 'error',
        'message': "Sorry something went wrong"
    })

@shop.route('/api/getInventory', methods=['POST'])
def getInventory():
    data = request.json
    user_id= data['user_id']
    inventory = Inventory.query.filter_by(user_id = user_id).all()
    print(inventory)
    return jsonify([i.to_dict() for i in inventory])

@shop.route('/api/deleteItem', methods=['POST'])
def deleteItem():
    data = request.json
    user_id = data['user_id']
    item_name= data['item_name']
    print(user_id)
    # user = User.query.filter_by(id= user_id)

    inventory= Inventory.query.filter_by(user_id = user_id).filter_by(name=item_name).first()
    print(inventory, 'inventory')
    

    
    
    
    db.session.delete(inventory)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': f'item has been removed'
    })





