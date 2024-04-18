from app import db
from models.employee import Employee

class Manager(Employee):
  id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)

  def __init__(self, username, password, name, email, phone, imageUrl=None, xUrl=None, linkedinUrl=None, salary=None, active_status=None, usr_id=None):
    if usr_id is None:
      super().__init__(username, password, name, email, phone, "manager", imageUrl, xUrl, linkedinUrl, salary, active_status)
    else:
      super().__init__(username, password, name, email, phone, "manager", imageUrl, xUrl, linkedinUrl, salary, active_status, usr_id=usr_id)

  def __repr__(self):
    return f"Manager: {self.name}"