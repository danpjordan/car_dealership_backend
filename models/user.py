from app import db
from datetime import datetime
import bcrypt
from app import db
import random

class User(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  username = db.Column(db.String(200),unique=True)
  password = db.Column(db.String(200))
  active_status = db.Column(db.String(1))
  role = db.Column(db.String(10), default="customer")
  timeCreated = db.Column(db.DateTime, nullable=False)

  def __repr__(self):
    return f"User: {self.username}"

  def __init__(self, username, password, role="customer"):
    self.id = self.generate_unique_id()
    self.username = username
    self.password = bcrypt.hashpw((password).encode('utf-8'), 
                    bcrypt.gensalt()).decode('utf-8')
    self.active_status = 'Y'
    self.timeCreated = datetime.now();
    
    if role is not None:
      self.role = role
    
  def generate_unique_id(self):
    while True:
      random_id = random.randint(100000, 999999)
      exisitng_user = User.query.filter_by(id=random_id).first()
      if not exisitng_user:
        return random_id
      
def format_user(user):
  return {
    "username" : user.username,
    "id": user.id,
    "role": user.role,
  }