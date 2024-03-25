from flask import Flask
from flask_smorest import Api

from Config import Config

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)

from resources.sale_receipt import bp as sale_receipt_bp
app.register_blueprint(sale_receipt_bp)
from resources.car import bp as car_bp
app.register_blueprint(car_bp)