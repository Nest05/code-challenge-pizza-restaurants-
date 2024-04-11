from app import app
from models import *

with app.app_context():

    Restaurant.query.delete()
    RestaurantPizza.query.delete()
    Pizza.query.delete()

    r1 = Restaurant(name='Dominion Pizza', address="Good Italian, Ngong Road, 5th Avenue")
    r2 = Restaurant(name='Pizza Hut', address="Westgate Mall, Mwanzi Road, Nrb 100")
    db.session.add_all([restaurant1, restaurant2])
    db.session.commit()

    p1 = Pizza(name='Cheese', ingredients="Dough, Tomato Sauce, Cheese")
    p2 = Pizza(name="Pepperoni", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
    db.session.add_all([p1, p2])
    db.session.commit()

    rp1 = RestaurantPizza(pizza=p1, restaurant=r1, price = 15)
    rp2 = RestaurantPizza(pizza=p2, restaurant=r2, price = 25)
    db.session.add_all([rp1, rp2])
    db.session.commit()

