from flask import request
from flask.views import MethodView
from uuid import uuid4

from schemas import CarSchema
from . import bp
from db import cars

@bp.route('/car')
class CarList(MethodView):
    
    @bp.response(200, CarSchema(many=True))
    def get(self):
        return list(cars.values())
    
    @bp.arguments(CarSchema)
    @bp.response(201, CarSchema)
    def post(self, data):
 
        car_id = uuid4().hex
        cars[car_id] = data
        return cars[car_id]

@bp.route('/car/<int:id>')
class Car(MethodView):
    
    @bp.response(200, CarSchema)
    def get(self, id):
        if id in cars:
            return cars[id]
        return {
            'UH OH, something went wrong' : "invalid car id"
        }, 400

    @bp.arguments(CarSchema)
    def put(self, data, id):
        data = request.get_json()
        if id in cars:
            cars[id] = data
            return { 'car updated' : cars[id] }, 201
        return {'err' : 'no car found with that id'}, 401

    def delete(self, id):
        
        if id in cars:
            del cars[id]
            return { 'car gone': f" is no more. . . " }, 202
        return { 'err' : "can't delete that car they aren't there. . . " } , 400
