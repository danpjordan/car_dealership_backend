from flask import jsonify, request
from models.user import *
from authentication.auth import *
from controllers.employee_controller import *
from controllers.car_controller import *
from controllers.customer_controller import *
from app import app, db

# create an employee
@app.route('/employees/', methods = ['POST'])
def create_employee_api():
 return create_employee()

# delete an employee
@app.route('/employees/<id>/', methods = ['DELETE'])
def delete_employee_api(id):
  return delete_employee(id)

# get single employee
@app.route('/employees/<id>/', methods = ['GET'])
def get_employee_api(id):
  return get_employee(id)

# edit an employee
@app.route('/employees/<id>/', methods = ['PUT'])
def update_employee_api(id):
  return update_employee(id)

# get all employees
@app.route('/employees/', methods = ['GET'])
def get_employees_api():
  return get_employees()

# create batch employees
@app.route('/batch-create-employees', methods=['POST'])
def batch_create_employees_api():
  return batch_create_employees()

# create a customer
@app.route('/customers/', methods = ['POST'])
def create_customer_api():
  return create_customer()

# delete a customer
@app.route('/customers/<id>/', methods = ['DELETE'])
def delete_customer_api(id):
  return delete_customer(id)

# get single customer
@app.route('/customers/<id>/', methods = ['GET'])
def get_customer_api(id):
  return get_customer(id)

# edit a customer
@app.route('/customers/<id>/', methods = ['PUT'])
def update_customer_api(id):
  return update_customer(id)

# get all customers
@app.route('/customers/', methods = ['GET'])
def get_customers_api():
  return get_customers()

# create batch customers
@app.route('/batch-create-customers', methods=['POST'])
def batch_create_customers_api():
  return batch_create_customers()

# create a car
@app.route('/cars/', methods = ['POST'])
def create_car_api():
  return create_car()
  
# delete a car
@app.route('/cars/<id>/', methods = ['DELETE'])
def delete_car_api(id):
  return delete_car(id)

# get single car
@app.route('/cars/<id>/', methods = ['GET'])
def get_car_api(id):
  return get_car(id)

# edit a car
@app.route('/cars/<id>/', methods = ['PUT'])
def update_car_api(id):
  return update_car(id)
  
# get all cars
@app.route('/cars/', methods = ['GET'])
def get_cars_api():
  return get_cars()

# create batch cars
@app.route('/batch-create-cars', methods=['POST'])
def batch_create_cars_api():
  return batch_create_cars()

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
def login_api():
  return login()
  
@app.route('/logout/', methods = ['GET'])
def logout_api():
  return logout()

@app.route('/users', methods = ['POST'])
def create_user_api():
  return create_user()

# define a route for testing
@app.route('/')
def hello():
  return "Shhh, ur not supposed to be here!"