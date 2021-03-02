from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# User Class/Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    favorites = db.relationship("Favorite", backref="user", lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User %r>" % self.username

    def serialize(self):
        return {"id": self.id, "username": self.username, "email": self.email}


# Planet Class/Model
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    population = db.Column(db.BigInteger)
    gravity = db.Column(db.String(40))
    climate = db.Column(db.String(50))
    terrain = db.Column(db.String(50))
    surface_water = db.Column(db.Integer)
    diameter = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    pic = db.Column(db.String(500))
    url = db.Column(db.String(100))

    def __init__(
        self,
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
    ):
        self.name = name
        self.population = population
        self.gravity = gravity
        self.climate = climate
        self.terrain = terrain
        self.surface_water = surface_water
        self.diameter = diameter
        self.orbital_period = orbital_period
        self.rotation_period = rotation_period
        self.pic = pic
        self.url = url

    def __repr__(self):
        return "<Planet %r>" % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "gravity": self.gravity,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "diameter": self.diameter,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period,
            "pic": self.pic,
            "url": self.url,
        }


# Person Class/Model
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True, nullable=False)
    birth_year = db.Column(db.String(50))
    homeworld = db.Column(db.String(40), db.ForeignKey(Planet.name))
    eye_color = db.Column(db.String(10))
    gender = db.Column(db.String(15))
    hair_color = db.Column(db.String(20))
    height = db.Column(db.Integer)
    mass = db.Column(db.Integer)
    skin_color = db.Column(db.String(20))
    pic = db.Column(db.String(500))
    url = db.Column(db.String(100))

    def __init__(
        self,
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
    ):
        self.name = name
        self.birth_year = birth_year
        self.homeworld = homeworld
        self.eye_color = eye_color
        self.gender = gender
        self.hair_color = hair_color
        self.height = height
        self.mass = mass
        self.skin_color = skin_color
        self.pic = pic
        self.url = url

    def __repr__(self):
        return "<Person %r>" % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "homeworld": self.homeworld,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "height": self.height,
            "mass": self.mass,
            "skin_color": self.skin_color,
            "pic": self.pic,
            "url": self.url,
        }


# Favorite Class/Model
class Favorite(db.Model):
    username = db.Column(db.String(100), db.ForeignKey("user.username"), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String(40))
    person_name = db.Column(db.String(25))

    def __init__(self, username, planet_name, person_name):
        self.username = username
        self.planet_name = planet_name
        self.person_name = person_name

    def __repr__(self):
        return "<Favorite %r>" % self.id

    def serialize(self):
        return {
            "username": self.username,
            "id": self.id,
            "planet_name": self.planet_name,
            "person_name": self.person_name,
        }
