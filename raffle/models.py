from raffle import db, login_manager
from flask_login import UserMixin

# Get user by id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Database Model
class User(db.Model, UserMixin):    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwd = db.Column(db.String(300), nullable=False, unique=True)

    def __repr__(self):
        return f"{self.username}, {self.email}"