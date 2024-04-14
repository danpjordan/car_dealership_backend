from flask import jsonify, request
from authentication.auth import *
from controllers.car_controller import *
from controllers.customer_controller import *
from controllers.salesrep_controller import *
from controllers.manager_controller import *
from app import app, db

@app.route('/managers/', methods = ['POST'])
def create_manager_api():
  return create_manager()

@app.route('/managers/<id>/', methods = ['DELETE'])
def delete_manager_api(id):
  return delete_manager(id)

@app.route('/managers/<id>/', methods = ['GET'])
def get_manager_api(id):
  return get_manager(id)

@app.route('/managers/<id>/', methods = ['PUT'])
def update_manager_api(id):
  return update_manager(id)

@app.route('/managers/', methods = ['GET'])
def get_managers_api():
  return get_managers()

@app.route('/batch-create-managers/', methods=['POST'])
def batch_create_managers_api():
  return batch_create_managers()

@app.route('/salesreps/', methods = ['POST'])
def create_salesrep_api():
  return create_salesrep()

@app.route('/salesreps/<id>/', methods = ['DELETE'])
def delete_salesrep_api(id):
  return delete_salesrep(id)

@app.route('/salesreps/<id>/', methods = ['GET'])
def get_salesrep_api(id):
  return get_salesrep(id)

@app.route('/salesreps/<id>/', methods = ['PUT'])
def update_salesrep_api(id):
  return update_salesrep(id)

@app.route('/salesreps/', methods = ['GET'])
def get_all_salesreps_api():
  return get_all_salesreps()

@app.route('/batch-create-salesreps/', methods=['POST'])
def batch_create_salesreps_api():
  return batch_create_salesreps()

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
@app.route('/batch-create-cars/', methods=['POST'])
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
  print(login())
  return login()
  
@app.route('/logout/', methods = ['GET'])
def logout_api():
  return logout()

@app.route('/users/', methods = ['POST'])
def create_user_api():
  return create_user()

# define a route for testing
@app.route('/')
def hello():
  return "Shhh, ur not supposed to be here!"