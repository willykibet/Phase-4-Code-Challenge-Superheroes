from app import app, db, Hero, Power, HeroPower
import random
from sqlalchemy import func

with app.app_context():
    print("🦸‍♀️ Seeding powers...")
    powers_data = [
        {"name": "super strength", "description": "gives the wielder super-human strengths"},
        {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
        {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
        {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
    ]
    powers = [Power(**data) for data in powers_data]
    db.session.add_all(powers)
    db.session.commit()
    print("🦸‍♀️ Powers seeded!")

    print("🦸‍♀️ Seeding heroes...")
    heroes_data = [
        {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
        {"name": "Doreen Green", "super_name": "Squirrel Girl"},
        {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
        {"name": "Janet Van Dyne", "super_name": "The Wasp"},
        {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
        {"name": "Carol Danvers", "super_name": "Captain Marvel"},
        {"name": "Jean Grey", "super_name": "Dark Phoenix"},
        {"name": "Ororo Munroe", "super_name": "Storm"},
        {"name": "Kitty Pryde", "super_name": "Shadowcat"},
        {"name": "Elektra Natchios", "super_name": "Elektra"}
    ]
    heroes = [Hero(**data) for data in heroes_data]
    db.session.add_all(heroes)
    db.session.commit()
    print("🦸‍♀️ Heroes seeded!")

    def seed_hero_powers():
        print("🦸‍♀️ Adding powers to heroes...")
        strengths = ["Strong", "Weak", "Average"]
        heroes = Hero.query.all()

        try:
            for hero in heroes:
                for _ in range(random.randint(1, 3)):
                    power = Power.query.order_by(func.random()).first()
                    strength = random.choice(strengths)

                    hero_power = HeroPower(hero=hero, power=power, strength=strength)
                    db.session.add(hero_power)

            db.session.commit()
            print("🦸‍♀️ Powers added to heroes!")

        except Exception as e:
            print(f"Error: {str(e)}")
            db.session.rollback()

    if __name__ == "__main__":
        seed_hero_powers()
        print("🦸‍♀️ Done seeding!")