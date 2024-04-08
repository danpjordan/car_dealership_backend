from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)

# Set up the SQLAlchemy configuration for the PostgreSQL database
# Replace the sensitive information with environment variables in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:6569@localhost:5433/car-dealership'
db = SQLAlchemy(app)
CORS(app)

# Define the Employees model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    imageUrl = db.Column(db.String(400), nullable=False)
    xUrl = db.Column(db.String(400))
    linkedinUrl = db.Column(db.String(400))

    def __repr__(self):
        return f"Employee: {self.name}"

    def __init__(self, name, role="Car salesperson", imageUrl="static.vecteezy.com/system/resources/thumbnails/020/765/399/small/default-profile-account-unknown-icon-black-silhouette-free-vector.jpg", xUrl="twitter.com", linkedinUrl="linkedin.com"):
        self.name = name;
        self.role = role;
        self.imageUrl = imageUrl;
        self.xUrl = xUrl;
        self.linkedinUrl = linkedinUrl;

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
    "linkedinUrl": employee.linkedinUrl
  }

# Define a route for testing
@app.route('/')
def hello():
    return "Hey!"
  
# create an employee
@app.route('/employees', methods = ['POST'])
def create_employee():
  name = request.json['name']
  role = request.json['role']
  imageUrl = request.json['imageUrl']
  xUrl = request.json['xUrl']
  linkedinUrl = request.json['linkedinUrl']
  
  employee = Employee(name, role, imageUrl, xUrl, linkedinUrl)
  db.session.add(employee)
  db.session.commit()
  return format_employee(employee)

#get all employees
@app.route('/employees', methods = ['GET'])
def get_employees():
  employees = Employee.query.order_by(Employee.id.asc()).all()
  employees_list = []
  for employee in employees:
    employees_list.append(format_employee(employee))
  return {'employees': employees_list}
  

if __name__ == '__main__':
    # Create the database tables based on the defined models
    with app.app_context():
      db.create_all()

    # Run the Flask application
    app.run(port=8000)
