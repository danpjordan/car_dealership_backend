from models.employee import Employee
from app import db

#inherit from employee
class Manager(Employee):
  
  def __repr__(self):
    return f"Manager: {self.name}"
  
  def __init__(self, name, username, password, emp_role=None, imageUrl=None, xUrl=None, linkedinUrl=None):
    super().__init__(name, username, password, "Manager", imageUrl, xUrl, linkedinUrl)
 


