from random import randint, choice as rc

from faker import Faker

from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

fake = Faker()

with app.app_context():

    Restaurant.query.delete()
    Pizza.query.delete()
    RestaurantPizza.query.delete()

    restaurants = []
    for i in range(30):
        r = Restaurant(name=fake.city(), address = fake.address())
        restaurants.append(r)

    db.session.add_all(restaurants)

    pizzas = []
    for i in range(100):
        p = Pizza(
            name=fake.color_name(),
            ingredients="Dough, Tomato Sauce, Cheese, Pepperoni"
        )
        pizzas.append(p)

    db.session.add_all(pizzas)
    db.session.commit()
    
    restaurant_pizzas = []
    for i in range(200):
        p = rc(pizzas)
        r = rc(restaurants)
        
        pr = RestaurantPizza(
            price = randint(1, 30),
            pizza = rc(pizzas),
            restaurant = rc(restaurants)
        )
        restaurant_pizzas.append(pr)
    
    db.session.add_all(restaurant_pizzas)
    db.session.commit()
    