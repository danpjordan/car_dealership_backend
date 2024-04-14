from app import db
from models.user import User

class Employee(User):
  __abstract__ = True
  name = db.Column(db.VARCHAR(100), nullable=False)
  emp_role = db.Column(db.VARCHAR(100), nullable=False, default="Car Salesman")
  imageUrl = db.Column(db.VARCHAR(400), nullable=False, default="https://i.imgur.com/0S7YILp.jpeg")
  xUrl = db.Column(db.VARCHAR(400), nullable=False, default="https://twitter.com")
  linkedinUrl = db.Column(db.VARCHAR(400), nullable=False, default="https://www.linkedin.com")
  salary = db.Column(db.INTEGER, nullable=False, default=50000)
  # salary
  def __repr__(self):
    return f"Employee: {self.name}"

  def __init__(self, name, username, password, emp_role=None, imageUrl=None, xUrl=None, linkedinUrl=None):
    super().__init__(username, password, "employee")
    
    self.name = name
    if emp_role is not None:
      self.emp_role = emp_role
    if imageUrl is not None:
      self.imageUrl = imageUrl
    if xUrl is not None:
      self.xUrl = xUrl
    if linkedinUrl is not None:
      self.linkedinUrl = linkedinUrl
      
      
      