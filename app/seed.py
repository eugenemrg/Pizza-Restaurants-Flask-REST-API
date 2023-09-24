from random import randint, choice as rc

from faker import Faker

from app import app
from models import db, Restaurant, Pizza

fake = Faker()

with app.app_context():

    Restaurant.query.delete()
    Pizza.query.delete()

    restaurants = []
    for i in range(30):
        r = Restaurant(name=fake.city(), address = fake.address())
        restaurants.append(r)

    db.session.add_all(restaurants)

    pizzas = []
    for i in range(100):
        p = Pizza(
            name=fake.color_name(),
            ingredients="Dough, Tomato Sauce, Cheese, Pepperoni",
            price=randint(1, 30)
        )
        pizzas.append(p)

    db.session.add_all(pizzas)
    db.session.commit()
    