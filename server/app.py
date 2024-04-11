from flask import Flask, request, make_response
from flask_migrate import Migrate

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def home():
    return '<h1>PIZZA RESTAURANTS CODE CHALLENGE</h1>'

@app.route('/restaurants')
def restaurants():
    restaurants = [restaurant.to_dict() for restaurant in Restaurant.query.all()]
    return make_response(  restaurants,   200  )

@app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
def restaurants_by_id(id):

    restaurant = Restaurant.query.filter_by(id=id).first()

    if request.method == 'GET':
        restaurant_serialized = restaurant.to_dict()

        response = make_response ( 
            restaurant_serialized, 
            200  
        )

        return response
    
    elif request.method == 'DELETE':
        db.session.delete(restaurant)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Baked good deleted."
        }

        response = make_response(
            response_body,
            200
        )

        return response
    

if __name__ == '__main__':
    app.run(port=5555, debug=True)