from models.employee import Employee
from app import db

class SalesRep(Employee):
  id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)
  manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'), nullable=False)

  def __repr__(self):
    return f"SalesRep: {self.name}"
  
  def __init__(self, username, password, name, manager_id, email=None, phone=None, imageUrl=None, xUrl=None, linkedinUrl=None, salary=None, active_status=None, usr_id=None):
    if usr_id is None:
      super().__init__(username, password, name, email, phone, "sales rep", imageUrl, xUrl, linkedinUrl, salary, active_status)
    else:
      super().__init__(username, password, name, email, phone, "sales rep", imageUrl, xUrl, linkedinUrl, salary, active_status, usr_id=usr_id)
    
    self.manager_id = manager_id;