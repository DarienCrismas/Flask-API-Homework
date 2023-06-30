from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = "")
    last_name = db.Column(db.String(150), nullable = True, default = '')    
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False, default = '')
    username = db.Column(db.String, nullable = False)
    token = db.Column(db.String, default = "", unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    card = db.relationship("Card", backref = "owner", lazy = True)


    def __init__(self, email, username, password, first_name = "", last_name = ""):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token()
        self.username = username 

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        return generate_password_hash(password)
    
    def set_token(self):
        return secrets.token_hex(24)
    
    def __repr__(self):
        return f"{self.username} has been added to the database."
    
class Card(db.Model):
    id = db.Column(db.String, primary_key = True)
    pokemon = db.Column(db.String(50))
    edition = db.Column(db.String(20), nullable = True)
    estimated_price = db.Column(db.Numeric(precision=10, scale=2), nullable = True)
    condition = db.Column(db.String(150), nullable = True)
    type = db.Column(db.String(20))
    promotional = db.Column(db.String(20))
    move_1 = db.Column(db.String(150))
    move_2 = db.Column(db.String(150))
    hit_points = db.Column(db.Numeric(5))
    user_token = db.Column(db.String, db.ForeignKey("user.token"), nullable = False)


    def __init__(self, pokemon, edition, estimated_price, condition, pokemon_type, promotional, move_1, move_2, hit_points, user_token):
        self.id = self.set_id()
        self.pokemon = pokemon
        self.edition = edition
        self.estimated_price = estimated_price
        self.condition = condition
        self.pokemon_type = pokemon_type
        self.promotional = promotional
        self.move_1 = move_1
        self.move_2 = move_2
        self.hit_points = hit_points
        self.user_token = user_token

    def set_id(self):
        return str(uuid.uuid4())
    
    def __repr__(self):
        return f"Your {self.pokemon} card has been added to the PokeBank"

class CardSchema(ma.Schema):
    class Meta:
        fields = ["id", "pokemon", "edition", "estimated_price", "condition", "pokemon_type", "promotional", "move_1", "move_2", "hit_points"]

card_schema = CardSchema()
bank_schema = CardSchema(many=True)
