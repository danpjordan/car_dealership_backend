from app import db
from models.employee import Employee
from models.user import User
class Manager(User):
  id = db.Column(db.INTEGER, db.ForeignKey('user.id'), primary_key=True)
  name = db.Column(db.VARCHAR(100), nullable=False)
  emp_role = db.Column(db.VARCHAR(100), nullable=False, default="Manager")
  imageUrl = db.Column(db.VARCHAR(400), nullable=False, default="https://i.imgur.com/0S7YILp.jpeg")
  xUrl = db.Column(db.VARCHAR(400), nullable=False, default="https://twitter.com")
  linkedinUrl = db.Column(db.VARCHAR(400), nullable=False, default="https://www.linkedin.com")
  # salary
  
  def __init__(self, name, username, password, emp_role=None, imageUrl=None, xUrl=None, linkedinUrl=None):
    super().__init__(name, username, password, emp_role, imageUrl, xUrl, linkedinUrl)
    self.name = name
    if emp_role is not None:
      self.emp_role = emp_role
    if imageUrl is not None:
      self.imageUrl = imageUrl
    if xUrl is not None:
      self.xUrl = xUrl
    if linkedinUrl is not None:
      self.linkedinUrl = linkedinUrl

  def __repr__(self):
    return f"Manager: {self.name}"
  
  
 
