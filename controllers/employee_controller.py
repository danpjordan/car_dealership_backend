from models.employee import Employee
from app import app, db

def format_employee(employee): 
  return {
    "name" : employee.name,
    "role": employee.role,
    "imageUrl": employee.imageUrl,
    "xUrl": employee.xUrl,
    "linkedinUrl": employee.linkedinUrl
  }

def get_employees():
  with app.app_context():
    customer_team_view = db.Table('customer_team_view', db.MetaData(), autoload_with=db.engine)
  
  employees = db.session.query(customer_team_view).order_by(customer_team_view.c.role.asc()).all()
  employee_list = []
  for employee in employees:
    employee_list.append(format_employee(employee))
  return {'employees': employee_list}
