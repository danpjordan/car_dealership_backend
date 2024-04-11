from flask import jsonify, request
from models.employee import Employee, format_employee
from models.car import *
from models.user import *
from authentication.auth import *

from app import app, db

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
  
  employee = Employee(name, role, imageUrl, xUrl, linkedinUrl)
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
    return {'employee': format_employee(employee)}
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
  
# get all cars
@app.route('/cars/', methods = ['GET'])
def get_cars():
  cars = Car.query.order_by(Car.timeCreated.asc()).all()
  cars_list = []
  for car in cars:
    cars_list.append(format_car(car))
  return {'cars': cars_list}

@app.route('/adminpage/', methods = ['GET'])
@user_middleware(['admin'])
def helloA():
  return "Hello admin!"

@app.route('/employeepage/', methods = ['GET'])
@user_middleware(['admin', 'employee'])
def helloE():
  return "Hello employee!"

@app.route('/customerpage/', methods = ['GET'])
@user_middleware(['admin', 'employee', 'customer'])
def helloC():
  return "Hello customer!"

@app.route('/login/', methods = ['POST'])
def login():
  user=None
  try:
    username = request.json.get('username')
    user=User.query.filter(
        User.username==username,
        User.active_status=='Y'
        ).first()
    if not user:
      return jsonify({'error': 'user not found'}, 200)
    if not bcrypt.checkpw(
      request.json.get('password').encode('utf-8'),
      user.password.encode('utf-8')
    ):
      return jsonify({'error': 'invalid password'}, 200)
    
  except Exception as e:
    return jsonify({'error': 'unsuccessful login', 'details': str(e)}), 400
  
  print("success")
  
  try:
    token = createToken(user)
    return setCookie(token)
  except Exception as e:
    return jsonify({'error': 'failed to create token', 'details': str(e)}), 400

@app.route('/logout/', methods = ['GET'])
def logout():
  try:
    return removeCookie()

  except Exception as e:
    return jsonify({'error': 'logout unsuccessful', 'details': str(e)}), 400

@app.route('/users', methods = ['POST'])
def create_user():
  data = request.json
  
  if ('username') not in data:
    return jsonify({'error': 'username not provided'}), 400
  if ('password') not in data:
    return jsonify({'error': 'password not provided'}), 400
   
  username = data.get('username')
  role = data.get('role')
  password = data.get('password')
  user = User(username, password, role)
  
  db.session.add(user)

  try:
    db.session.commit()
    return format_user(user)
  except Exception as e:
    db.session.rollback()
    return jsonify({'error': 'Error in create_employee()', 'details': str(e)}), 500
  finally:
    db.session.close()

# define a route for testing
@app.route('/')
def hello():
  return "Shhh, ur not supposed to be here!"