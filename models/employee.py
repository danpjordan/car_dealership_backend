import random
from datetime import datetime
from app import db

class Employee(db.Model):
  id = db.Column(db.INTEGER, primary_key=True)
  name = db.Column(db.VARCHAR(100), nullable=False)
  role = db.Column(db.VARCHAR(100), nullable=False, default="Car Salesman")
  imageUrl = db.Column(db.VARCHAR(400), nullable=False, default="https://i.imgur.com/0S7YILp.jpeg")
  xUrl = db.Column(db.VARCHAR(400), nullable=False, default="https://twitter.com")
  linkedinUrl = db.Column(db.VARCHAR(400), nullable=False, default="https://www.linkedin.com")
  timeCreated = db.Column(db.DateTime, nullable=False, default=datetime.now())

  def __repr__(self):
    return f"Employee: {self.name}"

  def __init__(self, name, role=None, imageUrl=None, xUrl=None, linkedinUrl=None, timeCreated=None):
      self.id = self.generate_unique_id()
      self.name = name
      if role is not None:
          self.role = role
      if imageUrl is not None:
          self.imageUrl = imageUrl
      if xUrl is not None:
          self.xUrl = xUrl
      if linkedinUrl is not None:
          self.linkedinUrl = linkedinUrl
      if timeCreated is not None:
          self.timeCreated = timeCreated
      
  def generate_unique_id(self):
      while True:
          random_id = random.randint(100000, 999999)
          is_employee = Employee.query.filter_by(id=random_id).first()
          if not is_employee:
              return random_id
