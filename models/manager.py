from app import db
from models.employee import Employee

class Manager(Employee):
  id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
  people_managed = db.Column(db.Integer)
  def __init__(self, name, username, password, emp_role=None, imageUrl=None, xUrl=None, linkedinUrl=None, people_managed=0):
    super().__init__(name, username, password, "Manager", imageUrl, xUrl, linkedinUrl)
    self.people_managed = people_managed

  def __repr__(self):
    return f"Manager: {self.name}"
  
  
 
