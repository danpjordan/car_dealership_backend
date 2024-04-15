from app import db
from models.user import User

class Customer(User):
  id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
  cus_name = db.Column(db.VARCHAR(100), nullable=False)
  email = db.Column(db.VARCHAR(100), nullable=False)
  phone = db.Column(db.VARCHAR(100), nullable=False)
  
  def __repr__(self):
    return f"Customer: {self.cus_name}"
  
  def __init__(self, name, username, password, email, phone, usr_id=None):
    if usr_id is None:
      super().__init__(username, password, "customer")
    else:
      super().__init__(username, password, "customer", usr_id)
    
    self.cus_name = name
    self.email = email
    self.phone = phone
