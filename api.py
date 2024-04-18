from authentication.auth import *
from controllers.car_controller import *
from controllers.customer_controller import *
from controllers.salesrep_controller import *
from controllers.manager_controller import *
from controllers.employee_controller import *
from controllers.purchase_controller import *

from app import app

@app.route('/managers/', methods = ['POST'])
def create_manager_api():
  return create_manager()

@app.route('/managers/<id>/', methods = ['DELETE'])
def delete_manager_api(id):
  return delete_manager(id)

@app.route('/managers/<id>/', methods = ['GET'])
def get_manager_api(id):
  return get_manager(id)

@app.route('/managers/', methods = ['GET'])
@user_middleware(['manager'])
def get_managers_api():
  return get_managers()

@app.route('/manager/user/', methods = ['GET'])
@user_middleware(['manager'])
def get_m_customer_api():
  return get_m_customer()

@app.route('/manager/salesreps/', methods = ['GET'])
@user_middleware(['manager'])
def get_m_salesreps_api():
  return get_m_salesreps()

@app.route('/manager/purchases/', methods = ['GET'])
@user_middleware(['manager'])
def get_m_purchases_api():
  return get_m_purchases()

@app.route('/manager/cars/', methods = ['GET'])
def get_m_cars_api():
  return get_all_cars()

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
def get_salesreps_api():
  return get_salesreps()

@app.route('/batch-create-salesreps/', methods=['POST'])
def batch_create_salesreps_api():
  return batch_create_salesreps()

@app.route('/salesrep/user/', methods = ['GET'])
@user_middleware(['sales rep'])
def get_s_customer_api():
  return get_s_customer()

@app.route('/salesrep/purchases/', methods = ['GET'])
@user_middleware(['sales rep'])
def get_s_purchases_api():
  return get_s_purchases()

@app.route('/salesrep/cars/', methods = ['GET'])
@user_middleware(['sales rep'])
def get_s_cars_api():
  return get_all_cars()


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


# get all customers
@app.route('/customers/', methods = ['GET'])
def get_customers_api():
  return get_customers()

# create batch customers
@app.route('/batch-create-customers', methods=['POST'])
def batch_create_customers_api():
  return batch_create_customers()

@app.route('/customer/purchases/', methods = ['GET'])
@user_middleware(['customer'])
def get_c_purchases_api():
  return get_c_purchases()



@app.route('/purchases/', methods = ['POST'])
def create_purchase_api():
  return create_purchase()

@app.route('/purchases/<id>/', methods = ['DELETE'])
def delete_purchase_api(id):
  return delete_purchase(id)

@app.route('/purchases/<id>/', methods = ['GET'])
def get_purchase_api(id):
  return get_purchase(id)

@app.route('/purchases/<id>/', methods = ['PUT'])
def update_purchase_api(id):
  return update_purchase(id)

# get all purchases
@app.route('/purchases/', methods = ['GET'])
def get_purchases_api():
  return get_purchases()

# create a lot of purchases
@app.route('/batch-create-purchases/', methods=['POST'])
def batch_create_purchases_api():
  return batch_create_purchases()

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
  
# get all unsold cars
@app.route('/cars/', methods = ['GET'])
def get_unsold_cars_api():
  return get_unsold_cars()

# create batch cars
@app.route('/batch-create-cars/', methods=['POST'])
def batch_create_cars_api():
  return batch_create_cars()

# get all employees
@app.route('/employees/', methods = ['GET'])
def get_employees_api():
  return get_employees()

@app.route('/login/', methods = ['POST'])
def login_api():
  return login()
  
@app.route('/logout/', methods = ['GET'])
def logout_api():
  return logout()

@app.route('/users/', methods = ['POST'])
def create_user_api():
  return create_user()

#adminpage for testing
@app.route('/adminpage/', methods = ['GET'])
@user_middleware(['manager'])
def helloA():
  return "Hello admin!"

# define a route for testing
@app.route('/')
def hello():
  return "Shhh, ur not supposed to be here!"