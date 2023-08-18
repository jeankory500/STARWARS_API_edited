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
from models import db, User, Fav, People,Planets
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

current_logged_user_id = 1

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)



@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_characters():
    allCharacters = People.query.all()
    result = [element.serialize() for element in allCharacters]
    return jsonify(result), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    json_text = jsonify(people_id)
    return json_text

@app.route('/planets', methods=['GET'])
def get_planetList():
    allPlanets = Planets.query.all()
    result = [element.serialize() for element in allPlanets]
    return jsonify(result), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planets(planet_id):
    json_text = jsonify(planet_id)
    return json_text

@app.route('/user', methods=['GET'])
def get_users():

    users = User.query.all()

    user_list = [
        {
            'id': user.id,
            'email': user.email
        }
        for user in users
    ]

    return jsonify(user_list), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify(message='User not found'), 404
    return jsonify(user.serialize())

#Fav Endpoints

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planets_id):
 
    user = User.query.get()

    new_favorite = Fav(user_id="", planet_id=planets_id)
    db.session.add(new_favorite)
    db.session.commit()

    response_body = {
        "msg": "Planet added successfully", 
        "favorite": new_favorite.serialize()
    }

    return jsonify(response_body), 200


#delete Endpoints 


#@app.route('/users', methods=['GET'])
#def get_favorites()


    

        

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
