from app import db
from models.user import User

class Employee(User):
  id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
  imageUrl = db.Column(db.VARCHAR(400), nullable=False, default="https://i.imgur.com/0S7YILp.jpeg")
  xUrl = db.Column(db.VARCHAR(400), nullable=False, default="https://twitter.com")
  linkedinUrl = db.Column(db.VARCHAR(400), nullable=False, default="https://www.linkedin.com")
  salary = db.Column(db.INTEGER, nullable=False, default=0)

  def __repr__(self):
    return f"Employee: {self.name}"

  def __init__(self, username, password, name, email=None, phone=None, role="employee", imageUrl=None, xUrl=None, linkedinUrl=None, salary=None, active_status=None, usr_id=None):
    
    if usr_id is None:
      super().__init__(username, password, name, email, phone, role, active_status)
    else:
      super().__init__(username, password, name, email, phone, role, active_status, usr_id=usr_id)
    
    if imageUrl is not None:
      self.imageUrl = imageUrl
    if xUrl is not None:
      self.xUrl = xUrl
    if linkedinUrl is not None:
      self.linkedinUrl = linkedinUrl
    if salary is not None:
      self.salary = salary
      
      
      