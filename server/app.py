from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Restaurant, Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eateries.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Index(Resource):

    def get(self):

        response_dict = {
            "index": "Pizza Restaurant RESTful API",
        }

        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response

api.add_resource(Index, '/')

class Restaurants(Resource):

    def get(self):
        Restaurant.query.all()
        response_dict_list = [r.to_dict() for r in Restaurant.query.all()]

        response = make_response(
            response_dict_list,
            200,
        )

        return response

    def post(self):

        new_record = Restaurant(
            name=request.form['name'],
            address=request.form['address'],
        )

        db.session.add(new_record)
        db.session.commit()

        response_dict = new_record.to_dict()

        response = make_response(
            jsonify(response_dict),
            201,
        )

        return response

api.add_resource(Restaurants, '/restaurants')

class RestaurantByID(Resource):

    def get(self, id):

        response_dict = Restaurant.query.filter_by(id=id).first().to_dict()

        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response

    def patch(self, id):

        record = Restaurant.query.filter_by(id=id).first()
        for attr in request.form:
            setattr(record, attr, request.form[attr])

        db.session.add(record)
        db.session.commit()

        response_dict = record.to_dict()

        response = make_response(
            jsonify(response_dict),
            200
        )

        return response

    def delete(self, id):

        record = Restaurant.query.filter_by(id=id).first()

        db.session.delete(record)
        db.session.commit()

        response_dict = {"message": "restaurant successfully deleted"}

        response = make_response(
            jsonify(response_dict),
            200
        )

        return response

api.add_resource(RestaurantByID, '/restaurants/<int:id>')

class Pizzas(Resource):

    def get(self):

        response_dict_list = [n.to_dict() for n in Pizza.query.all()]

        response = make_response(
            jsonify(response_dict_list),
            200,
        )

        return response

api.add_resource(Pizzas, '/pizzas')

class RestaurantPizzas(Resource):
    
    def post(self):

        pass

api.add_resource(RestaurantPizzas, '/restaurants_pizzas')


if __name__ == '__main__':
    app.run(port=5556, debug=True)