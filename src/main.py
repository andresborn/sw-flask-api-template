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
from models import db, User, Planet, Person, Favorite
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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


# Create User
@app.route("/user", methods=["POST"])
def create_user():

    username = request.json["username"]
    email = request.json["email"]

    check_username = User.query.filter_by(username=f"{username}").first()
    if check_username:
        return jsonify({"error": "Username already exists"}), 401
    
    check_email = User.query.filter_by(email=f"{email}").first()
    if check_email:
        return jsonify({"error": "Email already exists"}), 401

    new_user = User(username, email)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize()), 200


# Get User
@app.route("/user/<username>", methods=["GET"])
def get_user(username):
    current_user = User.query.filter_by(username=f"{username}").first()
    request_body = current_user.serialize()
    return jsonify(request_body), 200


# Create Planet
@app.route("/planet", methods=["POST"])
def create_planet():

    name = request.json["name"]
    rotation_period = request.json["rotation_period"]
    orbital_period = request.json["orbital_period"]
    diameter = request.json["diameter"]
    climate = request.json["climate"]
    gravity = request.json["gravity"]
    terrain = request.json["terrain"]
    surface_water = request.json["surface_water"]
    population = request.json["population"]
    pic = request.json["pic"]
    url = request.json["url"]

    check_planet = Planet.query.filter_by(name=f"{name}").first()
    if check_planet:
        return jsonify({"error": "Planet already exists"}), 401

    new_planet = Planet(
        name,
        population,
        gravity,
        climate,
        terrain,
        surface_water,
        diameter,
        orbital_period,
        rotation_period,
        pic,
        url,
    )

    db.session.add(new_planet)
    db.session.commit()

    return jsonify(new_planet.serialize()), 200


# Get Planet
@app.route("/planet/<id>", methods=["GET"])
def get_planet(id):
    current_planet = Planet.query.filter_by(id=f"{id}").first()
    request_body = current_planet.serialize()
    return jsonify(request_body), 200


# Get All Planets
@app.route("/planet", methods=["GET"])
def get_all_planets():

    all_planets = Planet.query.all()

    request_body = list(map(lambda planet: planet.serialize(), all_planets))

    return jsonify(request_body), 200


# Create Person
@app.route("/person", methods=["POST"])
def create_person():

    name = request.json["name"]
    birth_year = request.json["birth_year"]
    homeworld = request.json["homeworld"]
    eye_color = request.json["eye_color"]
    gender = request.json["gender"]
    hair_color = request.json["hair_color"]
    height = request.json["height"]
    mass = request.json["mass"]
    skin_color = request.json["skin_color"]
    pic = request.json["pic"]
    url = request.json["url"]

    check_person = Person.query.filter_by(name=f"{name}").first()
    if check_person:
        return jsonify({"error": "Person already exists"}), 401

    new_person = Person(
        name,
        birth_year,
        homeworld,
        eye_color,
        gender,
        hair_color,
        height,
        mass,
        skin_color,
        pic,
        url,
    )

    db.session.add(new_person)
    db.session.commit()

    return jsonify(new_person.serialize()), 200


# Get Person
@app.route("/person/<id>", methods=["GET"])
def get_person(id):
    current_person = Person.query.filter_by(id=f"{id}").first()
    request_body = current_person.serialize()
    return jsonify(request_body), 200


# Get All People
@app.route("/person", methods=["GET"])
def get_all_people():

    all_people = Person.query.all()
    request_body = list(map(lambda person: person.serialize(), all_people))
    return jsonify(request_body), 200


# Create Favorite
@app.route("/favorite", methods=["POST"])
def create_favorite():

    username = request.json["username"]
    planet_name = request.json["planet_name"]
    person_name = request.json["person_name"]

    # Prevent Favorite Duplicates
    favorites_list = Favorite.query.filter_by(username=f"{username}").all()
    favorites_list = list(map(lambda x: x.serialize(), favorites_list))
    check_if_favorite_exists = list(filter(lambda fav: fav['planet_name'] == planet_name or fav['person_name'] == person_name, favorites_list))
    if len(check_if_favorite_exists) > 0:
        return jsonify({"error": "Favorite already exists"}), 401

    new_favorite = Favorite(username, planet_name, person_name)

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify(new_favorite.serialize()), 200


# Get User Favorites
@app.route("/favorite/<username>", methods=["GET"])
def get_user_favorites(username):

    user_favorites = Favorite.query.filter_by(username=f"{username}").all()
    favorites_list = list(map(lambda favorite: favorite.serialize(), user_favorites))

    return jsonify(favorites_list), 200


# Delete Favorite
@app.route("/favorite/<username>/<id>", methods=["DELETE"])
def delete_favorite(username, id):

    favorite = Favorite.query.filter_by(username=f"{username}", id=f"{id}").first()

    if not favorite:
        return jsonify({"error": "Favorite does not exist"}), 401

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"deleted": favorite.serialize()})


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
