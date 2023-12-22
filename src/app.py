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
from models import db, User, Planets, People, Favoritos
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

# SELECT * FROM user; (traigo todo los usuarios)
@app.route('/user', methods=['GET'])
def handle_user():
    users = User.query.all()
    print(users)
    serialize_users = list(map(lambda item: item.serialize(), users))
    return jsonify({'msg': 'good', 'results': serialize_users}), 200
    
    # SELECT * FROM user WHERE id = 1; (traigo el usuario en la posicion 1)
    '''
    user = User.query.get(user_id) #En el Postman debo agregarle /n° para ver los datos de lo que quiero encontra
    serialize_users = user.serialize()
    '''
    # SELECT * FROM user WHERE is_active = True;

    '''users = User.query.filter_by(is_active = True)
    serialize_users = list(map(lambda x: x.serialize(), users))
    print(users)
    return jsonify({'msg': 'good', 'results': serialize_users}), 200
    '''
#GET de todos los Planetas
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    print(planets)
    serialize_planets = list(map(lambda item: item.serialize(), planets))

    return jsonify({'msg': 'ok', 'results': serialize_planets}), 200

#GET de un solo Planeta
@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_info_planets(planets_id):
    
    planets = Planets.query.filter_by(id=planets_id).first()
    return jsonify(planets.serialize()), 200

#GET de todos los Personajes
@app.route('/people', methods=['GET'])
def handle_people():
    people = People.query.all()
    print(people)
    serialize_people = list(map(lambda item: item.serialize(),serialize_people))

    return jsonify({'msg': 'ok', 'results': serialize_people}), 200

#GET de un Personaje
@app.route('/people/<int:people_id>', methods=['GET'])
def get_info_people(people_id):
    
    onepeople = People.query.filter_by(id=people_id).first()
    return jsonify(onepeople.serialize()), 200

#GET Favoritos
@app.route('/user/<int:user_id>/favoritos/', methods=['GET'])
def get_favoritos_user(user_id):
    
    user_favoritos = Favoritos.query.filter_by(user_id=user_id).all()
    serialize_results = list(map(lambda item: item.serialize(),user_favoritos))

    return jsonify(serialize_results), 200

#POST de un Usuario
@app.route('/signup', methods=['POST'])
def add_new_user():
    request_body = request.json
    new_user = User(id=request_body['id'], nombre=request_body['name'], contraseña=request_body['password'],mail=request_body['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'msg': 'El usuario'}),200

#POST de un Planeta
@app.route('/user/<int:user_id>/favoritos/planets', methods=['POST'])
def add_new_planet_favorito(user_id):
    request_body=request.json
    new_favorito_planet=Favoritos(user_id=user_id, planetas_id=request_body['planets_id'])
    db.session.add(new_favorito_planet)
    db.session.commit()
    user_planets=Favoritos.query.filter_by(user_id=user_id).first()
    print(user_planets)
    return jsonify(request_body),200

    #POST de un Personaje
@app.route('/user/<int:user_id>/favoritos/people', methods=['POST'])
def add_new_people_favorito(user_id):
    request_body=request.json
    new_favorito_people=Favoritos(user_id=user_id, people_id=request_body['people_id'])
    db.session.add(new_favorito_people)
    db.session.commit()
    user_people=Favoritos.query.filter_by(user_id=user_id).first()
    print(user_people)
    return jsonify(request_body),200

#DELETE de un Planeta
@app.route('/user/<int:user_id>/favoritos/planets', methods=['DELETE'])
def delete_planets_favorito(user_id):
    request_body=request.json
    query= Favoritos.query.filter_by(user_id=user_id,planets_id=request_body['planets_id']).first()
#Este if es para el manejo de errores, es lo que va a ver el usuario 
    if query is None:
        return jsonify({"msg":"No hubo coincidencias, no hay nada para eliminar"}),404
    db.session.delete(query)
    db.session.commit()
    
    #return envia un mensaje al usuario, 
    return jsonify({"msg":"El favorito ha sido eliminado correctamente"}),200

#DELETE de un Personale
@app.route('/user/<int:user_id>/favoritos/personajes', methods=['DELETE'])
def delete_people_favorito(user_id):
    request_body=request.json
    query= Favoritos.query.filter_by(user_id=user_id,people_id=request_body['people_id']).first()
    print(query)
#Este if es para el manejo de errores, es lo que va a ver el usuario 
    if query is None:
        return jsonify({'msg':'No hubo coincidencias, no hay nada para eliminar'}),404
    db.session.delete(query)
    db.session.commit()
    #return envia un mensaje al usuario, 
    return jsonify({'msg':'El favorito ha sido eliminado correctamente'}),200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
