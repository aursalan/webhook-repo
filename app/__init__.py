from flask import Flask
from flask_cors import CORS
from .extensions import mongo
from app.webhook.routes import webhook
import os
from dotenv import load_dotenv


# Creating our flask app
def create_app():
    load_dotenv()

    app = Flask(__name__)

    CORS(app)

    app.config["MONGO_URI"] = os.getenv("MONGO_URI")

    mongo.init_app(app)
    
    # registering all the blueprints
    app.register_blueprint(webhook)
    
    return app
