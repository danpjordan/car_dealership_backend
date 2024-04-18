from app import db
from models.user import User

class Customer(User):
  id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
  
  def __repr__(self):
    return f"Customer: {self.cus_name}"
  
  def __init__(self, username, password, name=None, email=None, phone=None, active_status=None, usr_id=None):
    if usr_id is None:
      super().__init__(username, password, name, email, phone, "customer", active_status=active_status, usr_id=usr_id)
    else:
      super().__init__(username, password, name, email, phone, "customer", active_status=active_status, usr_id=usr_id)