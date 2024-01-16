"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os

from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET', "POST"])
def handle_users():
    if request.method == "GET":
        response_body = {}
        results = {}
        users = db.session.execute(db.select(User)).scalars()
        results["users"] = [row.serialize() for row in users]
        if len(results["users"]) > 0:
            response_body["message"] = "User List"
            response_body['results'] = results
            return jsonify(response_body), 200
        response_body["message"] = "No users registered"
        return jsonify(response_body), 200
    if request.method == 'POST':
        data = request.json
        response_body = {}
        user = User(email = data.get('email'),
                     username = data.get("username"),
                     name = data.get('name'),
                     last_name = data.get("last_name"),
                     country = data.get("country"))
        db.session.add(user)
        db.session.commit()
        response_body['user'] = user.serialize()
        return response_body, 200
    

@app.route("/user/<int:user_id>", methods=["GET", "PUT", "DELETE"])
def handle_user(user_id):
    response_body = {}
    results = {}
    if request.method == "GET":
        user = db.session.get(User, user_id)
        if not user:
            response_body['message'] = "User doesn't exists"
            return response_body, 404
        results['user'] = user.serialize()
        response_body['message'] = 'User found'
        response_body['results'] = results
        return response_body, 200

@app.route("/planet", methods=["GET", "POST"])
def handle_planet():
    if request.method == "GET":
        response_body = {}
        results = {}
        users = db.session.execute(db.select(Planet)).scalars()
        results["planets"] = [row.serialize() for row in users]
        if len(results["planets"]) > 0:
            response_body["message"] = "Planet List"
            response_body['results'] = results
            return jsonify(response_body), 200
        response_body["message"] = "No planets registered"
        return jsonify(response_body), 200
    if request.method == 'POST':
        data = request.json
        response_body = {}
        planet = Planet(population = data.get('population'),
                     gravity = data.get("gravity"),
                     name = data.get('name'),
                     climate = data.get("climate"))
        db.session.add(planet)
        db.session.commit()
        response_body['planet'] = planet.serialize()
        return response_body, 200

@app.route("/character", methods=["GET", "POST"])
def handle_character():
    if request.method == "GET":
        response_body = {}
        results = {}
        users = db.session.execute(db.select(Character)).scalars()
        results["characters"] = [row.serialize() for row in users]
        if len(results["characters"]) > 0:
            response_body["message"] = "Character List"
            response_body['results'] = results
            return jsonify(response_body), 200
        response_body["message"] = "No characters registered"
        return jsonify(response_body), 200
    if request.method == 'POST':
        data = request.json
        response_body = {}
        character = Character(last_name = data.get('last_name'),
                     eye_color = data.get("eye_color"),
                     name = data.get('name'),
                     height = data.get("height"),
                     origin_planet = data.get("origin_planet"))
        db.session.add(character)
        db.session.commit()
        response_body['planet'] = character.serialize()
        return response_body, 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
