# Beispielmodell – kann mit SQLAlchemy o.ä. erweitert werden

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    
class Lehrjahr1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    beruf = db.Column(db.String(100))
    berufsschule = db.Column(db.Boolean, default=False)

class Lehrjahr2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    beruf = db.Column(db.String(100))
    berufsschule = db.Column(db.Boolean, default=False)

class Lehrjahr3(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    beruf = db.Column(db.String(100))
    berufsschule = db.Column(db.Boolean, default=False)

class Lehrjahr4(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    beruf = db.Column(db.String(100))
    berufsschule = db.Column(db.Boolean, default=False)

class ExcludedNames(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
