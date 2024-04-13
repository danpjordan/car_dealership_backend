from app import db
from models.user import User

#
class Customer(User):
  id = db.Column(db.INTEGER, db.ForeignKey('user.id'), primary_key=True)
  name = db.Column(db.VARCHAR(100), nullable=False)
  cars_purchased = db.Column(db.INTEGER, default=0)
  email = db.Column(db.VARCHAR(100), nullable=False)
  phone = db.Column(db.VARCHAR(100), nullable=False)
  
  def __repr__(self):
    return f"Customer: {self.name}"
  
  def __init__(self, name, username, password, email, phone):
    super().__init__(username, password, "customer")
    
    self.name = name
    self.email = email
    self.phone = phone
    self.cars_purchased = 0
    