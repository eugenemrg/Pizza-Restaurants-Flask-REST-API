from app import app
from models import Pizza, Restaurant, RestaurantPizza, db

class TestApp():
    
    def test_restaurants_route(self):
        response = app.test_client().get('/restaurants')
        assert(response.status_code == 200)
        
    def test_restaurants_route_returns_json(self):
        response = app.test_client().get('/restaurants')
        assert response.content_type == 'application/json'
    
    def test_pizzas_route(self):
        response = app.test_client().get('/pizzas')
        assert(response.status_code == 200)
    
    def test_pizzas_route_returns_json(self):
        response = app.test_client().get('/pizzas')
        assert response.content_type == 'application/json'