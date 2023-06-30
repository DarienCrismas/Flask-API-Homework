from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from card_inventory.forms import CardForm
from card_inventory.models import Card, db

site = Blueprint("site", __name__, template_folder = "site_templates")

@site.route("/")
def home():
    print("Test clear.")
    return render_template("index.html")


@site.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    cardform = CardForm()

    try:
        if request.method == "POST" and cardform.validate_on_submit():
            pokemon = cardform.pokemon.data
            edition = cardform.edition.data
            estimated_price = cardform.estimated_price.data
            condition = cardform.condition.data
            pokemon_type = cardform.pokemon_type.data
            promotional = cardform.promotional.data
            move_1 = cardform.move_1.data
            move_2 = cardform.move_2.data
            hit_points = cardform.hit_points.data
            user_token = current_user.token

            card = Card(pokemon, edition, estimated_price, condition, pokemon_type, 
                        promotional, move_1, move_2, hit_points, user_token)
            
            db.session.add(card)
            db.session.commit()

            return redirect(url_for("site.profile"))
    except:
        raise Exception("Card not added. Please check your submission.")


    user_token = current_user.token
    cards = Card.query.filter_by(user_token=user_token)
    return render_template("profile.html", form=cardform, cards = cards)