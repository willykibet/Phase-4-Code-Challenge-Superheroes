
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database and migrations
db.init_app(app)
migrate = Migrate(app, db)


# Routes
@app.route("/")
def home():
    return "Welcome to the Superhero API!"


@app.route("/heroes", methods=["GET"])
def get_heroes():
    heroes = Hero.query.all()
    heroes_data = [
        {"id": hero.id, "name": hero.name, "super_name": hero.super_name}
        for hero in heroes
    ]
    return jsonify(heroes_data)


@app.route("/heroes/<int:hero_id>", methods=["GET"])
def get_hero(hero_id):
    hero = Hero.query.get(hero_id)

    if hero is None:
        return jsonify({"error": "Hero not found"}), 404

    hero_data = {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        'powers': [{'id': hero_power.power.id, 'name': hero_power.power.name, 'description': hero_power.power.description, 'strength': hero_power.strength} for hero_power in hero.hero_powers]
    }

    return jsonify(hero_data)


@app.route("/powers", methods=["GET"])
def get_powers():
    powers = Power.query.all()
    powers_data = [
        {"id": power.id, "name": power.name, "description": power.description}
        for power in powers
    ]
    return jsonify(powers_data)


@app.route("/powers/<int:power_id>", methods=["GET"])
def get_power(power_id):
    power = Power.query.get(power_id)

    if power is None:
        return jsonify({"error": "Power not found"}), 404

    power_data = {"id": power.id, "name": power.name, "description": power.description}

    return jsonify(power_data)


# Validation for HeroPower strength
VALID_STRENGTH_VALUES = ["Strong", "Weak", "Average"]


@app.route("/hero_powers", methods=["POST"])
def create_hero_power():
    data = request.json

    if "strength" not in data or "power_id" not in data or "hero_id" not in data:
        return jsonify({"errors": ["validation errors"]}), 400

    # Validate strength value
    if data["strength"] not in VALID_STRENGTH_VALUES:
        return jsonify({"errors": ["Invalid strength value"]}), 400

    hero = Hero.query.get(data["hero_id"])
    power = Power.query.get(data["power_id"])

    if hero is None or power is None:
        return jsonify({"error": "Hero or Power not found"}), 404

    hero_power = HeroPower(hero=hero, power=power, strength=data["strength"])

    try:
        db.session.add(hero_power)
        db.session.commit()
        return get_hero(hero.id)  # Return hero data with updated powers
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400


# Validation for Power description
@app.route("/powers/<int:power_id>", methods=["PATCH"])
def update_power(power_id):
    power = Power.query.get(power_id)

    if power is None:
        return jsonify({"error": "Power not found"}), 404

    data = request.json

    if "description" in data:
        if len(data["description"]) < 20:
            return (
                jsonify(
                    {"errors": ["Description must be at least 20 characters long"]}
                ),
                400,
            )

        power.description = data["description"]

    try:
        db.session.commit()
        return jsonify(
            {"id": power.id, "name": power.name, "description": power.description}
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5555)