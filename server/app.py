#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants_dict_list = [p.to_dict() for p in Plant.query.all()]
        response = make_response(
            plants_dict_list,
            200
        )
        return response
    def post(self):
        plant_json = request.get_json()
        new_plant = Plant(
            name=plant_json.get("name"),
            image=plant_json.get("image"),
            price=plant_json.get("price"),
        )
        db.session.add(new_plant)
        db.session.commit()
        plant_dict = new_plant.to_dict()
        response = make_response(
            plant_dict,
            201
        )
        return response
api.add_resource(Plants, '/plants')

class PlantsByID(Resource):
    def get(self, id):
        plant_dict = Plant.query.filter_by(id=id).first().to_dict()
        response = make_response(
            plant_dict,
            200
        )
        return response
    
api.add_resource(PlantsByID, '/plants/<int:id>')

    

class PlantByID(Resource):
    pass
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
