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
from models import db, People, Planet, User, Favorites
import json


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
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





@app.route('/people', methods=['GET'])
def get_all_people():

    people = People.query.all() 
    total_people = list(map(lambda item: item.serialize(), people))

    return jsonify(total_people), 200

#planet endpoints 

@app.route('/planets', methods=['GET'])
def get_all_planets():

    planets = Planet.query.all() 
    total_planets = list(map(lambda item: item.serialize(), planets))

    return jsonify(total_planets), 200



@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):

    person = People.query.filter_by(id=people_id).first()

    return jsonify(person.serialize()), 200



@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planet(planets_id):

    planet = Planet.query.filter_by(id=planets_id).first()

    return jsonify(planet.serialize()), 200


#user endpoints

@app.route('/users', methods=['GET'])
def get_users():

    users = User.query.all() 
    total_users = list(map(lambda item: item.serialize(), users))

    return jsonify(total_users), 200

@app.route('/users', methods=['POST'])
def create_user():
    body = json.loads(request.data) 
    

    query_user = User.query.filter_by(email=body["email"]).first() 
    if query_user is None:
        new_user = User(first_name=body["first_name"], last_name=body["last_name"], email=body["email"], password=body["password"], username=body["username"])
        db.session.add(new_user)
        db.session.commit()

        response_body = {
            "msg": "Created user"
        }
        return jsonify(response_body), 200

    response_body = {
            "msg": "existed user"
        }
    return jsonify(response_body), 400

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):

    user = User.query.filter_by(id=user_id).first()

    return jsonify(user.serialize()), 200

@app.route('/users/<int:user_id>/favorite', methods=['GET'])
def get_favorite(user_id):

    
    favorite = Favorites.query.filter_by(user_id=user_id).all()
    total_favorites = list(map(lambda item: item.serialize(), favorite))

    return jsonify(total_favorites), 200

#creating favorites planets 
@app.route('/users/<int:user_id>/favorites/planet', methods=['POST'])
def create_favorite_planet(user_id):
    body = json.loads(request.data) 
    
    query_favorite_planet = Favorites.query.filter_by(planet_id=body["planet_id"], user_id=body["user_id"]).first() 
    print(query_favorite_planet)
    
    if query_favorite_planet is None:
        new_favorite_planet = Favorites(user_id=body["user_id"], planet_id=body["planet_id"], people_id=body["people_id"])
        db.session.add(new_favorite_planet)
        db.session.commit()

        response_body = {
            "msg": "Created favorite planet"
        }
        return jsonify(response_body), 200

    response_body = {
            "msg": "existed favorite planet"
        }
    return jsonify(response_body), 400



@app.route('/users/<int:user_id>/favorites/people', methods=['POST'])
def create_favorite_people(user_id):
    body = json.loads(request.data) 
    
    query_favorite_people = Favorites.query.filter_by(people_id=body["people_id"], user_id=body["user_id"]).first() 
    print(query_favorite_people)
    
    if query_favorite_people is None:
        new_favorite_people = Favorites(user_id=body["user_id"], planet_id=body["planet_id"], people_id=body["people_id"])
        db.session.add(new_favorite_people)
        db.session.commit()

        response_body = {
            "msg": "Created favorite character"
        }
        return jsonify(response_body), 200

    response_body = {
            "msg": "existed favorite character"
        }
    return jsonify(response_body), 400

@app.route('/users/<int:user_id>/favorites/planet', methods=['DELETE'])
def delete_favorite_planet(user_id):
    body = json.loads(request.data)
    
    query_favorites_planet = Favorites.query.filter_by(planet_id=body["planet_id"], user_id=user_id).first()
    
    if query_favorites_planet is not None:
        db.session.delete(query_favorites_planet)
        db.session.commit()

        response_body = {
            "msg": "Deleted favorite planet"
        }
        return jsonify(response_body), 200

    response_body = {
        "msg": "Favorite planet does not exist"
    }
    return jsonify(response_body), 400


@app.route('/users/<int:user_id>/favorites/people', methods=['DELETE'])
def delete_favorite_people(user_id):
    body = json.loads(request.data)
    query_favorite_people = Favorites.query.filter_by(people_id=body["people_id"], user_id=user_id).first()
    
    if query_favorite_people is not None:
        db.session.delete(query_favorite_people)
        db.session.commit()

        response_body = {
            "msg": "Deleted favorite people"
        }
        return jsonify(response_body), 200

    response_body = {
        "msg": "Favorite character does not exist"
    }
    return jsonify(response_body), 400









 


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)