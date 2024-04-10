import random
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)

POSTGRES={
    'user':'postgres',
    'pw':'6569',
    'db':'car-dealership',
    'host':'localhost',
    'port':'5433'
}

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s'%POSTGRES
db = SQLAlchemy(app)
CORS(app)

class Employee(db.Model):
  id = db.Column(db.INTEGER, primary_key=True)
  name = db.Column(db.VARCHAR(100), nullable=False)
  role = db.Column(db.VARCHAR(100), nullable=False, default="Car Salesman")
  imageUrl = db.Column(db.VARCHAR(400), nullable=False, default="https://i.imgur.com/0S7YILp.jpeg")
  xUrl = db.Column(db.VARCHAR(400), nullable=False, default="https://twitter.com")
  linkedinUrl = db.Column(db.VARCHAR(400), nullable=False, default="https://www.linkedin.com")
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
  
# create an employee
@app.route('/employees/', methods = ['POST'])
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
    return jsonify({'error': 'Error in create_employee()', 'details': str(e)}), 500
  finally:
    db.session.close()

# delete an employee
@app.route('/employees/<id>/', methods = ['DELETE'])
def delete_employee(id):
  employee = db.session.get(Employee, id)
  if not employee:
    return jsonify({"error": "Employee not found"}), 404
  try:
    db.session.delete(employee)
    db.session.commit()
    return f'Employee (id: {id}) deleted!'
  except Exception as e:
    return jsonify({'error': 'Error in delete_employee()', 'details': str(e)}), 500
  finally:
    db.session.close()

# get single employee
@app.route('/employees/<id>/', methods = ['GET'])
def get_employee(id):
  employee = db.session.get(Employee, id)
  if not employee:
    return jsonify({"error": "Employee not found"}), 404

  return {'employee': format_employee(employee)}

# edit an employee
@app.route('/employees/<id>/', methods = ['PUT'])
def update_employee(id):
  employee = db.session.get(Employee, id)
  if not employee:
      return jsonify({"error": "Employee not found"}), 404
  
  data = request.json
  employee.name = data.get('name', employee.name)
  employee.role = data.get('role', employee.role)
  employee.imageUrl = data.get('imageUrl', employee.imageUrl)
  employee.xUrl = data.get('xUrl', employee.xUrl)
  employee.linkedinUrl = data.get('linkedinUrl', employee.linkedinUrl)
  employee.timeCreated = data.get('timeCreated', employee.timeCreated)

  try:
    db.session.commit()
    return {'': format(employee)}
  except Exception as e:
    return jsonify({'error': 'Error in edit_employee()', 'details': str(e)}), 500
  finally:
    db.session.close()

# get all employees
@app.route('/employees/', methods = ['GET'])
def get_employees():
  employees = Employee.query.order_by(Employee.timeCreated).all()
  employees_list = []
  for employee in employees:
    employees_list.append(format_employee(employee))
  return {'employees': employees_list}

class Car(db.Model):
  id = db.Column(db.INTEGER, primary_key=True)
  vin = db.Column(db.VARCHAR(17), nullable=False)
  make = db.Column(db.VARCHAR(100), nullable=False, default="Contact dealership")
  model = db.Column(db.VARCHAR(100), nullable=False, default="Contact dealership")
  year = db.Column(db.INTEGER, nullable=False, default=0)
  imageUrl = db.Column(db.VARCHAR(400), nullable=False, default="https://i.imgur.com/BBtjbgI.jpg")
  price = db.Column(db.DECIMAL(8,2), nullable=False, default=0)
  miles = db.Column(db.INTEGER, nullable=False, default=0)
  description = db.Column(db.VARCHAR(2000), nullable=False, default="Contact dealership")
  timeCreated = db.Column(db.DateTime, nullable=False, default=datetime.now())
  
  def __repr__(self):
    return f"Car: {self.model} {self.make} {self.year}"

  def __init__(self, vin, imageUrl, make=None, model=None, year=None, price=None, miles=None, description=None, timeCreated=None):
      self.id = self.generate_unique_id()
      self.vin = vin
      if imageUrl is not None:
          self.imageUrl = imageUrl
      if make is not None:
          self.make = make
      if model is not None:
          self.model = model
      if year is not None:
          self.year = year
      if price is not None:
          self.price = price
      if miles is not None:
          self.miles = miles
      if description is not None:
          self.description = description
      if timeCreated is not None:
          self.timeCreated = timeCreated
          
  def generate_unique_id(self):
      while True:
          random_id = random.randint(1000, 9999)
          is_car = Employee.query.filter_by(id=random_id).first()
          if not is_car:
              return random_id

# format car
def format_car(car):
  return {
    "id" : car.id,
    "vin" : car.vin,
    "make" : car.make,
    "model" : car.model,
    "year" : car.year,
    "imageUrl" : car.imageUrl,
    "price" : car.price,
    "miles" : car.miles,
    "description" : car.description,
    "timeCreated" : car.timeCreated
  }

# create a car
@app.route('/cars/', methods = ['POST'])
def create_car():
  data = request.json
  if ('vin') not in data:
    return jsonify({'error': 'vin attribute not provided'}), 400
  
  vin = data.get('vin')
  make = data.get('make')
  model = data.get('model')
  year = data.get('year')
  imageUrl = data.get('imageUrl')
  price = data.get('price')
  miles = data.get('miles')
  description = data.get('description')
  
  car = Car(vin, imageUrl, make, model, year, price, miles, description)
  db.session.add(car)
  
  try:
    db.session.commit()
    return format_car(car)
  except Exception as e:
    db.session.rollback()
    return jsonify({'error': 'Error in create_car()', 'details': str(e)}), 500
  finally:
    db.session.close()
  
# delete a car
@app.route('/cars/<id>/', methods = ['DELETE'])
def delete_car(id):
  car = db.session.get(Car, id)
  if not car:
    return jsonify({"error": "Car not found"}), 404
  try:
    db.session.delete(car)
    db.session.commit()
    return f'Car (id: {id}) deleted!'
  except Exception as e:
    return jsonify({'error': 'Error in delete_car()', 'details': str(e)}), 500
  finally:
    db.session.close()

# get single car
@app.route('/cars/<id>/', methods = ['GET'])
def get_car(id):
  car = db.session.get(Car, id)
  if not car:
    return jsonify({"error": "Car not found"}), 404

  return {'car': format_car(car)}

# edit a car
@app.route('/cars/<id>/', methods = ['PUT'])
def update_car(id):
  car = db.session.get(Car, id)
  if not car:
    return jsonify({"error": "Car not found"}), 404

  data = request.json
  car.vin = data.get('vin', car.vin)
  car.make = data.get('make', car.make)
  car.model = data.get('model', car.model)
  car.year = data.get('year', car.year)
  car.imageUrl = data.get('imageUrl', car.imageUrl)
  car.price = data.get('price', car.price)
  car.miles = data.get('miles', car.miles)
  car.description = data.get('description', car.description)
  car.timeCreated = data.get('timeCreated', car.timeCreated)

  try:
    db.session.commit()
    return {'Car': format(car)}
  except Exception as e:
    return jsonify({'error': 'Error in edit_car()', 'details': str(e)}), 500
  finally:
    db.session.close()
  
# get all employees
@app.route('/cars/', methods = ['GET'])
def get_cars():
  cars = Car.query.order_by(Car.timeCreated.asc()).all()
  cars_list = []
  for car in cars:
    cars_list.append(format_car(car))
  return {'cars': cars_list}




# define a route for testing
@app.route('/')
def hello():
  return "Hey!"

if __name__ == '__main__':
  with app.app_context():
    db.create_all()
  app.run(port=8000)
