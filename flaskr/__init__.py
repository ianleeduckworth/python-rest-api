import os
from flask import Flask
from flask import request
from flask_pymongo import PyMongo
from bson.json_util import dumps

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    app.config["MONGO_URI"] = "mongodb+srv://admin:admin@testcluster-kfc0g.mongodb.net/customers_db?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
    mongo = PyMongo(app)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.donfig.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    standard_schema = {
        "_id": 0,
        "address": 1,
        "name": 1
    }

    @app.route("/hello")
    def hello():
        return "Hello World!"

    @app.route("/allCustomers")
    def all_customers():
        customers = mongo.db.customers.find({}, standard_schema)
        return dumps(customers)

    @app.route("/customerByName")
    def customer_by_name():
        name = request.args.get('username')
        customer = mongo.db.customers.find_one({"name": name}, standard_schema)
        return dumps(customer)

    @app.route("/addressByName")
    def address_by_name():
        name = request.args.get('username')
        address = mongo.db.customers.find_one({"name": name}, {"_id": 0, "address": 1})

        if address is None:
            return "Address not found for username: " + name

        return address["address"]


    return app