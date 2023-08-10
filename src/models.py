from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association table for many-to-many relationship between User and People
user_favorite_people = db.Table('user_favorite_people',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('people_id', db.Integer, db.ForeignKey('people.id'), primary_key=True)
)

# Association table for many-to-many relationship between User and Planet
user_favorite_planet = db.Table('user_favorite_planet',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('planet_id', db.Integer, db.ForeignKey('planet.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    
    # Relationships
    favorite_people = db.relationship('People', secondary=user_favorite_people, backref=db.backref('favorited_by', lazy='dynamic'))
    favorite_planets = db.relationship('Planet', secondary=user_favorite_planet, backref=db.backref('favorited_by', lazy='dynamic'))

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    hair_color = db.Column(db.String(50), nullable=False)
    birth_year = db.Column(db.String(50), nullable=False)
    eye_color = db.Column(db.String(50), nullable=False)

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    terrain = db.Column(db.String(50), nullable=False)
    gravity = db.Column(db.String(50), nullable=False)
    climate = db.Column(db.String(50), nullable=False)
