from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()

class RestaurantPizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column('pizza_id', db.Integer, db.ForeignKey('pizza.id'))
    restaurant_id = db.Column('restaurant_id', db.Integer, db.ForeignKey('restaurant.id'))
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    restaurant = db.relationship('Restaurant', back_populates='pizzas')
    pizza = db.relationship('Pizza', back_populates='restaurants')
        
    @validates('price')
    def validate_price(self, key, price):
        price_check = int(price)
        if price_check < 1 or price_check > 30:
            raise ValueError('Price must be between 1 and 30')
        return price
    
    def __repr__(self):
        return f'<RestaurantPizza, pizza id: {self.pizza_id}, restaurant id: {self.restaurant_id}, price: {self.price}> '
      
class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    
    pizzas = db.relationship('RestaurantPizza', back_populates='restaurant')
        
    @validates('name')
    def validate_name(self, key, name):
        restaurants = Restaurant.query.filter_by(name=name).first()
        if restaurants is None and name.strip().count(' ') > 49:
            raise ValueError('Name must have less than 50 words in length and be unique')
        elif restaurants is not None:
            raise ValueError('Name must be unique')
        return name
    
    def __repr__(self):
        return f'<Restaurant, name:{self.name} address:{self.address}>'

class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    restaurants = db.relationship('RestaurantPizza', back_populates='pizza')
    
    def __repr__(self):
        return f'<Pizza, name: {self.name} ingredients: {self.ingredients}'