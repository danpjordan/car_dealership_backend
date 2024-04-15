from app import db
from models.employee import Employee

class Manager(Employee):
  id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)

  def __init__(self, name, username, password, imageUrl=None, xUrl=None, linkedinUrl=None, usr_id=None):
    if usr_id is None:
      super().__init__(name, username, password, "Manager", imageUrl, xUrl, linkedinUrl)
    else:
      super().__init__(name, username, password, "Manager", imageUrl, xUrl, linkedinUrl, usr_id)

  def __repr__(self):
    return f"Manager: {self.name}"