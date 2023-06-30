from flask import Blueprint, request, jsonify
from card_inventory.helpers import token_required
from card_inventory.models import db, Card, card_schema, bank_schema

api = Blueprint('api', __name__, url_prefix="/api")

@api.route("/getdata")
def getdata():
    return {"some": "value"}

@api.route("/cards", methods = ["POST"])
@token_required
def add_card(our_user):
    pokemon = request.json["pokemon"]
    edition = request.json["edition"]
    estimated_price = request.json["estimated_price"]
    condition = request.json["condition"]
    pokemon_type = request.json["pokemon_type"]
    promotional = request.json["promotional"]
    move_1 = request.json["move_1"]
    move_2 = request.json["move_2"]
    hit_points = request.json["hit_points"]
    user_token = our_user.token

    print(f"User Token: {our_user.token}")

    card = Card(pokemon, edition, estimated_price, condition, pokemon_type, 
                 promotional, move_1, move_2, hit_points, user_token)

    db.session.add(card)
    db.session.commit()

    response = card_schema.dump(card)
    return jsonify(response)

@api.route("/cards/<id>", methods = ["GET"])
@token_required
def get_card(our_user, id):
    if id:
        card = Card.query.get(id)
        response = card_schema.dump(card)
        return jsonify(response)
    else:
        return jsonify("message:", "Missing ID"), 401
    

@api.route("/cards", methods=["GET"])
@token_required
def get_cards(our_user):
    token = our_user.token
    cards = Card.query.filter_by(user_token = token).all()
    response = bank_schema.dump(cards)
    return jsonify(response)


@api.route("/cards/<id>", methods = ["PUT"])
@token_required
def alter_card(our_user, id):
    card = Card.query.get(id)
    card.pokemon = request.json["pokemon"]
    card.edition = request.json["edition"]
    card.estimated_price = request.json["estimated_price"]
    card.condition = request.json["condition"]
    card.pokemon_type = request.json["pokemon_typ"]
    card.promotional = request.json["promotional"]
    card.move_1 = request.json["move_1"]
    card.move_2 = request.json["move_2"]
    card.hit_points = request.json["hit_points"]
    card.user_token = our_user.token

    db.session.commit()
    response = card_schema.dump(card)
    return jsonify(response)


@api.route("/cards/<id>", methods = ["DELETE"])
@token_required
def remove_card(our_user, id):
    card = Card.query.get(id)
    db.session.delete(card)
    db.session.commit()

    response = card_schema.dump(card)
    return jsonify(response)
