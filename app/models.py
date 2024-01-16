# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    super_name = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)

    # Relationship with HeroPower
    hero_powers = db.relationship('HeroPower', backref='powers_hero')

class Power(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)  

    # Relationship with HeroPower
    hero_powers = db.relationship('HeroPower', backref='powers_power')

class HeroPower(db.Model):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)
    strength = db.Column(db.Integer, nullable=False)

    # Relationships
    hero = db.relationship('Hero', backref='powers_hero', foreign_keys=[hero_id])
    power = db.relationship('Power', backref='powers_power', foreign_keys=[power_id])