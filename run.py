from app import app,db
from app.models import Product, User, Inventory, Post

# when you open up a flask shell it's gonna make sure the database is connected
@app.shell_context_processor
def shell_context():
    return {'db': db, 'User' : User, 'Product': Product, "Inventory": Inventory, 'Post': Post}

if __name__ == '__main__':
    app.run()