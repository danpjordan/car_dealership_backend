from models.employee import Employee
from app import db
from models.user import User

class SalesRep(User):
  id = db.Column(db.INTEGER, db.ForeignKey('user.id'), primary_key=True)
  name = db.Column(db.VARCHAR(100), nullable=False)
  imageUrl = db.Column(db.VARCHAR(400), nullable=False, default="https://i.imgur.com/0S7YILp.jpeg")
  xUrl = db.Column(db.VARCHAR(400), nullable=False, default="https://twitter.com")
  linkedinUrl = db.Column(db.VARCHAR(400), nullable=False, default="https://www.linkedin.com")

  #test change
  def __repr__(self):
    return f"SalesRep: {self.name}"
  
  def __init__(self, name, username, password, imageUrl=None, xUrl=None, linkedinUrl=None):
    super().__init__(name, username, password, "SalesRep", imageUrl, xUrl, linkedinUrl)
    self.name = name
    if imageUrl is not None:
      self.imageUrl = imageUrl
    if xUrl is not None:
      self.xUrl = xUrl
    if linkedinUrl is not None:
      self.linkedinUrl = linkedinUrl
   
      