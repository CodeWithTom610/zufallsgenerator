# Beispielmodell – kann mit SQLAlchemy o.ä. erweitert werden

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    Beruf = db.Column(db.String(50), nullable=False)
    lehrjahr = db.Column(db.Integer, nullable=False)
    nicht_da = db.Column(db.Boolean, default=False)
