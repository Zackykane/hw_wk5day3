from flask import request, jsonify, json
from flask.views import MethodView
from flask_smorest import abort
from uuid import uuid4

from . import bp
from schemas import SaleReceiptsSchema
from db import cars, sale_receipts

@bp.route('/sale_receipt')
class SaleReceiptList(MethodView):
    
    @bp.arguments(SaleReceiptsSchema)
    def post(self, sale_receipt_data):
        if sale_receipt_data['sale'] not in cars:
            return {"message": "user does not exist"}, 400
        sale_receipt_id = uuid4().hex
        sale_receipts[sale_receipt_id] = sale_receipt_data

        return {
            'message': "Sale_receipt created",
            'sale_receipt_id': sale_receipt_id
            }, 201

    @bp.response(200, SaleReceiptsSchema(many=True))
    def get(self):
        return list(sale_receipts.values())

@bp.route('/sale_receipt/<sale_receipt_id>')
class SaleReceipt(MethodView):

    @bp.response(200, SaleReceiptsSchema)
    def get(self, sale_receipt_id):
        try: 
            return sale_receipts[sale_receipt_id]
        except KeyError:
            return {'message':"invalid post"}, 400

    @bp.arguments(SaleReceiptsSchema)
    def put(self, sale_receipt_data, sale_receipt_id):
        if sale_receipt_id in sale_receipts:
            sale_receipts[sale_receipt_id] = {k:v for k,v in sale_receipt_data.items() if k != 'id'} 

            return {'message': f'sale_receipt: {sale_receipt_id} updated'}, 201
        
        return {'message': "invalid sale_receipt"}, 400

    def delete(self, sale_receipt_id):

        if sale_receipt_id not in sale_receipts:
            return { 'message' : "Invalid sale_receipt"}, 400
        
        sale_receipts.pop(sale_receipt_id)
        return {'message': f'Sale_receipt: {sale_receipt_id} deleted'}