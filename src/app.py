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
from models import db, User, People, Planet

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

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200

# User Endpoints
@app.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users])

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.serialize())

# People Endpoints
@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    return jsonify([person.name for person in people])

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    if person:
        return jsonify(person.name)
    return jsonify({"error": "Not Found"}), 404

# Planets Endpoints
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.name for planet in planets])

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        return jsonify(planet.name)
    return jsonify({"error": "Not Found"}), 404

# Add a new favorite person to the current user
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    person = Person.query.get(people_id)
    if not person:
        return jsonify({"error": "Person not found"}), 404

    # Using first user as a placeholder
    user = User.query.first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Check if this favorite already exists
    existing_favorite = db.session.query(favorites).filter_by(
        user_id=user.id, entity_id=people_id, entity_type="person"
    ).first()
    if existing_favorite:
        return jsonify({"error": "Favorite already exists"}), 400

    # Add to favorites
    new_favorite = {"user_id": user.id, "entity_id": people_id, "entity_type": "person"}
    db.session.add(favorites, new_favorite)
    db.session.commit()
    return jsonify({"success": "Favorite added"}), 200

# Delete favorite planet for current user
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    # Using first user as a placeholder
    user = User.query.first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    favorite = db.session.query(favorites).filter_by(
        user_id=user.id, entity_id=planet_id, entity_type="planet"
    ).first()
    if not favorite:
        return jsonify({"error": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"success": "Favorite deleted"}), 200


# Delete favorite person for current user
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    # Using first user as a placeholder
    user = User.query.first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    favorite = db.session.query(favorites).filter_by(
        user_id=user.id, entity_id=people_id, entity_type="person"
    ).first()
    if not favorite:
        return jsonify({"error": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"success": "Favorite deleted"}), 200


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
