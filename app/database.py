from flask_pymongo import PyMongo

mongo = PyMongo()

def initialize_db(app):
    app.config["MONGO_URI"] = "mongodb://localhost:27017/MyDatabase"
    mongo.init_app(app)
