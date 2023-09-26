from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_marshmallow import Marshmallow
from models import db, Restaurant, Pizza, RestaurantPizza
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eateries.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Restaurants REST API 1.0"
    }
)

app.register_blueprint(swaggerui_blueprint)

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

ma = Marshmallow(app)

class PizzaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'ingredients')
        include_fk = True

pizza_schema = PizzaSchema()

class RestaurantSchema(ma.SQLAlchemySchema):
    class Meta:
        fields = ('id', 'name', 'address', 'pizzas')
        include_fk = True
        
    pizzas =  ma.Nested(PizzaSchema, many=True)

restaurant_schema = RestaurantSchema()

class RestaurantsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'address')
        include_fk = True

restaurants_schema = RestaurantsSchema()

class RestaurantPizzaSchema(ma.Schema):
    class Meta:
        fields = ('price', 'pizza_id', 'restaurant_id')
        # include_fk = True

pr_schema = RestaurantPizzaSchema()

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
        response_dict_list = [restaurants_schema.dump(r) for r in Restaurant.query.all()]

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

        response_dict = restaurant_schema.dump(new_record)

        response = make_response(
            jsonify(response_dict),
            201,
        )

        return response

api.add_resource(Restaurants, '/restaurants')

class RestaurantByID(Resource):

    def get(self, id):
        
        r = Restaurant.query.filter_by(id=id).first()
        
        if r is None:
            return make_response(
                jsonify({ "error": "Restaurant not found" }),
                404
            )

        response_dict = restaurant_schema.dump(r)

        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response

    def delete(self, id):

        r = Restaurant.query.filter_by(id=id).first()
         
        if r is None:
            return make_response(
                jsonify({ "error": "Restaurant not found" }),
                404
            )

        db.session.delete(r)
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

        response_dict_list = [pizza_schema.dump(n) for n in Pizza.query.all()]

        response = make_response(
            jsonify(response_dict_list),
            200,
        )

        return response

api.add_resource(Pizzas, '/pizzas')

class RestaurantPizzas(Resource):
    
    def post(self):
        
        pr = RestaurantPizza(
            pizza_id=int(request.form['pizza_id']), 
            restaurant_id=int(request.form['restaurant_id']), 
            price=int(request.form['price'])
        )

        db.session.add(pr)
        db.session.commit()
        db.session.refresh(pr)
        
        if RestaurantPizza.query.filter(RestaurantPizza.id == pr.id).first() is None:
            return make_response(jsonify({ "errors": ["validation errors"] }), 200)
            
        response_dict = pizza_schema.dump(pr.pizza)

        response = make_response(
            jsonify(response_dict),
            201,
        )

        return response

api.add_resource(RestaurantPizzas, '/restaurant_pizzas')


if __name__ == '__main__':
    app.run(port=5555, debug=True)