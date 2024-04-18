import random
from datetime import datetime
from app import db
from models.employee import Employee

class Car(db.Model):
  id = db.Column(db.INTEGER, primary_key=True)
  vin = db.Column(db.VARCHAR(17), nullable=False, unique=True)
  make = db.Column(db.VARCHAR(100), nullable=False, default="Contact dealership")
  model = db.Column(db.VARCHAR(100), nullable=False, default="Contact dealership")
  year = db.Column(db.INTEGER, nullable=False, default=0)
  imageUrl = db.Column(db.VARCHAR(400), nullable=False, default="https://i.imgur.com/BBtjbgI.jpg")
  price = db.Column(db.DECIMAL(8,2), nullable=False, default=0)
  miles = db.Column(db.INTEGER, nullable=False, default=0)
  description = db.Column(db.VARCHAR(2000), nullable=False, default="Contact dealership")
  timeCreated = db.Column(db.DateTime, nullable=False)
  is_sold = db.Column(db.VARCHAR(1), nullable=False, default="N")
  
  def __repr__(self):
    return f"Car: {self.model} {self.make} {self.year}"

  def __init__(self, vin, make=None, model=None, year=None, imageUrl=None, price=None, miles=None, description=None, car_id=None, is_sold=None):
    if car_id is None:
      self.id = self.generate_unique_id()
    else:
      self.id = car_id
      
    self.vin = vin
    self.timeCreated = datetime.utcnow()
    if imageUrl is not None:
      self.imageUrl = imageUrl
    if make is not None:
      self.make = make
    if model is not None:
      self.model = model
    if year is not None:
      self.year = year
    if price is not None:
      self.price = price
    if miles is not None:
      self.miles = miles
    if description is not None:
      self.description = description
    if imageUrl is not None:
      self.is_sold = is_sold
          
  def generate_unique_id(self):
    while True:
      random_id = random.randint(1000, 9999)
      is_car = Employee.query.filter_by(id=random_id).first()
      if not is_car:
        return random_id

