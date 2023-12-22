from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    #Como quedan las tablas
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favoritos_user= db.relationship('Favoritos', backref='user', lazy=True)
    #Cuando le hago print
    def __repr__(self):
        return '{}'.format(self.email) 

    #Como voy a convertir esa información de CLASE a OBJETO 
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
        }
    #SI modifico estructura de la tabla correr los codigos -> $ pipenv run migrate, $ pipenv run upgrade
    #TABLA DE PLANETAS
class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    climate = db.Column(db.String(100), nullable=False)
    planets_user= db.relationship('Favoritos', backref='planets', lazy=True)
    
    def __repr__(self):
        return '{}'.format(self.name)

    def serialize(self):
         return{
           "id": self.id,
           "name": self.name,
           "climate": self.climate,
    }

#TABLA DE PERSONAJES
class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.String(20))
    people_user= db.relationship('Favoritos', backref='people', lazy=True)

    def __repr__(self):
        return '{}'.format(self.name)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "height": self.height,
        }

#TABLA DE FAVORITOS
class Favoritos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))  
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))              

    def __repr__(self):
        return 'Favoritos with name {}'.format(self.id)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "favoritos_id": self.favoritos_id,
            "planets_id": self.planets_id,
        }   

#SI agrego una tabla correr los codigos -> $ pipenv run migrate, $ pipenv run upgrade