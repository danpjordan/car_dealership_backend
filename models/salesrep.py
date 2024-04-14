from models.employee import Employee
from app import db

class SalesRep(Employee):
  id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
  number_of_sales = db.Column(db.Integer)
  #test change
  def __repr__(self):
    return f"SalesRep: {self.name}"
  
  def __init__(self, name, username, password, imageUrl=None, xUrl=None, linkedinUrl=None):
    super().__init__(name, username, password, "SalesRep", imageUrl, xUrl, linkedinUrl)
    self.number_of_sales = 0