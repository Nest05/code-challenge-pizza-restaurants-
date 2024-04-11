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
            "restaurant_pizzas": "Baked good deleted."
        }

        response = make_response(
            response_body,
            200
        )

        return response
    
@app.route('/pizzas')
def pizzas():
    pizzas = [pizza.to_dict() for pizza in Pizza.query.all()]
    return make_response(  pizzas,   200  )

@app.route('/restaurant_pizzas', methods=['GET', 'POST'])
def restaurant_pizzas():
    if request.method == 'GET':
        restaurant_pizzas = [restaurant_pizzas.to_dict() for restaurant_pizzas in RestaurantPizza.query.all()]
        return make_response( restaurant_pizzas, 200 )
    
    elif request.method == 'POST':
        new_restaurant_pizzas = restaurant_pizzas(
            price=request.form.get("price"),
            pizza_id=request.form.get("pizza_id"),
            restaurant_id=request.form.get("restaurant_id"),
        )

        db.session.add(new_restaurant_pizzas)
        db.session.commit()

        response = make_response(new_restaurant_pizzas.to_dict(), 201)
        return response

    

if __name__ == '__main__':
    app.run(port=5555, debug=True)