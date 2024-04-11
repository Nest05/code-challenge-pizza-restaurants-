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
    

if __name__ == '__main__':
    app.run(port=5555, debug=True)