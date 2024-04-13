from app import db
from models.employee import Employee

class Manager(Employee):
  def __init__(self, name, username, password, emp_role=None, imageUrl=None, xUrl=None, linkedinUrl=None):
    super().__init__(name, username, password, emp_role, imageUrl, xUrl, linkedinUrl)
 
  def __repr__(self):
    return f"Manager: {self.name}"
  
 
