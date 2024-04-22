from app import db
from datetime import datetime
import bcrypt
from app import db
import random

class User(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  username = db.Column(db.String(200),unique=True)
  password = db.Column(db.String(200))
  active_status = db.Column(db.String(1), default='Y')
  role = db.Column(db.String(10), default="user")
  timeCreated = db.Column(db.DateTime, nullable=False)
  name = db.Column(db.VARCHAR(100))
  email = db.Column(db.VARCHAR(100))
  phone = db.Column(db.VARCHAR(100))

  def __repr__(self):
    return f"User: {self.username}"

  def __init__(self, username, password, name=None, email=None, phone=None, role=None, active_status=None, usr_id=None):
    if usr_id is None:
      self.id = self.generate_unique_id()
    else:
      self.id = usr_id
    
    self.username = username
    self.password = bcrypt.hashpw((password).encode('utf-8'), 
                    bcrypt.gensalt()).decode('utf-8')
    self.timeCreated = datetime.utcnow()
    
    if name is not None:
      self.name = name
    if email is not None:
      self.email = email
    if phone is not None:
      self.phone = phone
    if role is not None:
      self.role = role
    if active_status is not None:
      self.active_status = active_status
  
  def generate_unique_id(self):
    while True:
      random_id = random.randint(100000, 999999)
      exisitng_user = User.query.filter_by(id=random_id).first()
      if not exisitng_user:
        return random_id