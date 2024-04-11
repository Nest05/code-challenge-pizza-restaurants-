from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


from sqlalchemy.orm import validates

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    serialize_rules = ('-resturantpizzas.restaurant',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)  # set the maximum length
    address = db.Column(db.String)

    resturantpizzas = db.relationship('RestaurantPizza', back_populates='restaurant')
    @validates('name')
    def validate_name(self, key, name):
        if len(name) > 50:
            raise ValueError('Name must be less than 50 characters')
        existing_restaurant = Restaurant.query.filter_by(name=name).first()
        if existing_restaurant:
            raise ValueError('Name must be unique')
        return name


class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    serialize_rules = ('-resturantpizzas.pizza',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    resturantpizzas = db.relationship('RestaurantPizza', back_populates='pizza')


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'resturantpizzas'

    serialize_rules = ('-restaurant.resturantpizzas', '-pizza.resturantpizzas',)

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)

    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))

    pizza = db.relationship('Pizza', back_populates='resturantpizzas')
    restaurant = db.relationship('Restaurant', back_populates='resturantpizzas')

    @validates('price')
    def validate_price(self, key, price):
        if not 1 <= int(price[0]) <= 30:
            raise ValueError('Price must be between 1 and 30')
        return price

    def __repr__(self):
        return f'<Price = {self.price}>'