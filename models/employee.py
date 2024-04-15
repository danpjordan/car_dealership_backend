from app import db
from models.user import User

class Employee(User):
  id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
  name = db.Column(db.VARCHAR(100), nullable=False)
  imageUrl = db.Column(db.VARCHAR(400), nullable=False, default="https://i.imgur.com/0S7YILp.jpeg")
  xUrl = db.Column(db.VARCHAR(400), nullable=False, default="https://twitter.com")
  linkedinUrl = db.Column(db.VARCHAR(400), nullable=False, default="https://www.linkedin.com")
  salary = db.Column(db.INTEGER, nullable=False, default=0)

  def __repr__(self):
    return f"Employee: {self.name}"

  def __init__(self, name, username, password, role="employee", imageUrl=None, xUrl=None, linkedinUrl=None, usr_id=None):
    
    if id is None:
      super().__init__(username, password, role)
    else:
      super().__init__(username, password, role, usr_id)
    self.name = name
    if imageUrl is not None:
      self.imageUrl = imageUrl
    if xUrl is not None:
      self.xUrl = xUrl
    if linkedinUrl is not None:
      self.linkedinUrl = linkedinUrl
      
      
      