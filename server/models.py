from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Restaurant(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    
    # pizzas = db.relationship('Pizza', secondary='restaurant_pizza', backref='restaurants')

    def __repr__(self):
        return f'<Restaurant: {self.name} located at: {self.address}>'

class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    def __repr__(self):
        return f'<Pizza: ({self.name}) has {self.ingredients}>'

# class RestaurantPizza(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
    
#     restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
#     pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'))
#     price = db.Column(db.Float)
#     created_at = db.Column(db.DateTime, server_default=db.func.now())
#     updated_at = db.Column(db.DateTime, onupdate=db.func.now())

#     restaurant = db.relationship('Restaurant', back_populates=db.backref('restaurant_pizzas', cascade='all, delete-orphan'))
#     pizza = db.relationship('Pizza', back_populates=db.backref('restaurant_pizzas', cascade='all, delete-orphan'))
    
#     def __repr__(self):
#         return f'RestaurantPizza(restaurant_id={self.restaurant_id}, ' + \
#             f'pizza_id={self.pizza_id})'