from models.employee import Employee
from app import db

class SalesRep(Employee):
  id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)
  manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'), nullable=False)

  def __repr__(self):
    return f"SalesRep: {self.name}"
  
  def __init__(self, name, username, manager_id, password, imageUrl=None, xUrl=None, linkedinUrl=None, usr_id=None):
    if usr_id is None:
      super().__init__(name, username, password, "Sales Rep", imageUrl, xUrl, linkedinUrl)
    else:
      super().__init__(name, username, password, "Sales Rep", imageUrl, xUrl, linkedinUrl, usr_id)
    
    self.manager_id = manager_id;