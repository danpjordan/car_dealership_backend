import random
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:6569@localhost:5433/car-dealership'
db = SQLAlchemy(app)
CORS(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False, default="Car Salesman")
    imageUrl = db.Column(db.String(400), nullable=False, default="https://i.imgur.com/0S7YILp.jpeg")
    xUrl = db.Column(db.String(400), default="https://twitter.com")
    linkedinUrl = db.Column(db.String(400), default="https://www.linkedin.com")
    timeCreated = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return f"Employee: {self.name}"

    def __init__(self, name, role=None, imageUrl=None, xUrl=None, linkedinUrl=None, timeCreated=None):
        self.id = self.generate_unique_id()
        self.name = name
        if role is not None:
            self.role = role
        if imageUrl is not None:
            self.imageUrl = imageUrl
        if xUrl is not None:
            self.xUrl = xUrl
        if linkedinUrl is not None:
            self.linkedinUrl = linkedinUrl
        if timeCreated is not None:
            self.timeCreated = timeCreated
        
    def generate_unique_id(self):
        while True:
            random_id = random.randint(100000, 999999)
            is_employee = Employee.query.filter_by(id=random_id).first()
            if not is_employee:
                return random_id

# get single employee
@app.route('/employees/<id>', methods = ['GET'])
def get_employee(id):
  employee = Employee.query.filter_by(id=id).one()
  return {'employees': format_employee(employee)}

# delete an employee
@app.route('/employees/<id>', methods = ['DELETE'])
def delete_employee(id):
  employee = Employee.query.filter_by(id=id).one()
  db.session.delete(employee)
  db.session.commit()
  return f'Employee (id: {id}) deleted!'

# edit an employee
@app.route('/employees/<id>', methods = ['PUT'])
def update_employee(id):
  employee = Employee.query.get(id)
  if not employee:
      return jsonify({"error": "Employee not found"}), 404
  
  data = request.json
  employee.name = data.get('name', employee.name)
  employee.role = data.get('role', employee.role)
  employee.imageUrl = data.get('imageUrl', employee.imageUrl)
  employee.xUrl = data.get('xUrl', employee.xUrl)
  employee.linkedinUrl = data.get('linkedinUrl', employee.linkedinUrl)
  employee.timeCreated = data.get('timeCreated', employee.timeCreated)

  db.session.commit()
  return {'Employees': format(employee)}

# format employees
def format_employee(employee):
  return {
    "name" : employee.name,
    "id": employee.id,
    "role": employee.role,
    "imageUrl": employee.imageUrl,
    "xUrl": employee.xUrl,
    "linkedinUrl": employee.linkedinUrl,
    "timeCreated" : employee.timeCreated
  }

# define a route for testing
@app.route('/')
def hello():
    return "Hey!"
  
# create an employee
@app.route('/employees', methods = ['POST'])
def create_employee():
  
  data = request.json
  if ('name') not in data:
    return jsonify({'error': 'name attribute not provided'}), 400
  
  name = data.get('name')
  role = data.get('role')
  imageUrl = data.get('imageUrl')
  xUrl = data.get('xUrl')
  linkedinUrl = data.get('linkedinUrl')
  timeCreated = data.get('timeCreated')
  
  employee = Employee(name, role, imageUrl, xUrl, linkedinUrl, timeCreated)
  db.session.add(employee)
  try:
    db.session.commit()
    return format_employee(employee)
  except Exception as e:
    db.session.rollback()
    return jsonify({'error': 'Error on create_employee()', 'details': str(e)}), 500
  finally:
    db.session.close()

# get all employees
@app.route('/employees', methods = ['GET'])
def get_employees():
  employees = Employee.query.order_by(Employee.timeCreated).all()
  employees_list = []
  for employee in employees:
    employees_list.append(format_employee(employee))
  return {'employees': employees_list}
  

if __name__ == '__main__':
    with app.app_context():
      db.create_all()

    app.run(port=8000)
