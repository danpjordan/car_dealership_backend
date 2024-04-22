from authentication.auth import *
from controllers.car_controller import *
from controllers.customer_controller import *
from controllers.salesrep_controller import *
from controllers.manager_controller import *
from controllers.employee_controller import *
from controllers.purchase_controller import *
from controllers.user_controller import *
from app import app

'''User APIs'''
@app.route('/user/', methods = ['PUT', 'PATCH'])
@user_middleware(['customer', 'sales rep', 'manager'])
def update_user_api():
  return update_user()

@app.route('/user/deactivate', methods = ['GET'])
@user_middleware(['customer', 'sales rep', 'manager'])
def deactivate_user_api():
  return deactivate_user()

@app.route('/user/', methods = ['GET'])
@user_middleware(['customer', 'sales rep', 'manager'])
def get_user_api():
  return get_user()


'''Manager APIs'''
@app.route('/managers/', methods = ['POST'])
def create_manager_api():
  return create_manager()

@app.route('/managers/', methods = ['GET'])
@user_middleware(['manager'])
def get_managers_api():
  return get_managers()

@app.route('/manager/customers/', methods = ['GET'])
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

@app.route('/manager/purchases/total/', methods = ['GET'])
@user_middleware(['manager'])
def get_m_purchases_total_api():
  return get_m_purchases_total()

@app.route('/manager/cars/', methods = ['GET'])
def get_m_cars_api():
  return get_all_cars()

@app.route('/batch-create-managers/', methods=['POST'])
def batch_create_managers_api():
  return batch_create_managers()


'''Sales Rep APIs'''
@app.route('/salesreps/', methods = ['POST'])
def create_salesrep_api():
  return create_salesrep()

@app.route('/salesreps/', methods = ['GET'])
def get_salesreps_api():
  return get_salesreps()

@app.route('/batch-create-salesreps/', methods=['POST'])
def batch_create_salesreps_api():
  return batch_create_salesreps()

@app.route('/salesrep/customers/', methods = ['GET'])
@user_middleware(['sales rep'])
def get_s_customer_api():
  return get_s_customer()

@app.route('/salesrep/purchases/', methods = ['GET'])
@user_middleware(['sales rep'])
def get_s_purchases_api():
  return get_s_purchases()

@app.route('/salesrep/purchases/total/', methods = ['GET'])
@user_middleware(['sales rep'])
def get_s_purchases_total_api():
  return get_s_purchases_total()

@app.route('/salesrep/cars/', methods = ['GET'])
@user_middleware(['sales rep'])
def get_s_cars_api():
  return get_all_cars()


'''Customer APIs'''
@app.route('/customers/', methods = ['POST'])
def create_customer_api():
  return create_customer()

@app.route('/customers/', methods = ['GET'])
def get_customers_api():
  return get_customers()

@app.route('/batch-create-customers', methods=['POST'])
def batch_create_customers_api():
  return batch_create_customers()

@app.route('/customer/purchases/', methods = ['GET'])
@user_middleware(['customer'])
def get_c_purchases_api():
  return get_c_purchases()


'''Purchase APIs'''
@app.route('/purchases/', methods = ['POST'])
def create_purchase_api():
  return create_purchase()

@app.route('/purchases/', methods = ['GET'])
def get_purchases_api():
  return get_purchases()

@app.route('/batch-create-purchases/', methods=['POST'])
def batch_create_purchases_api():
  return batch_create_purchases()


'''Car APIs'''
@app.route('/cars/', methods = ['POST'])
def create_car_api():
  return create_car()
  
@app.route('/cars/', methods = ['GET'])
def get_unsold_cars_api():
  make = request.args.get('make')
  model = request.args.get('model')
  year = request.args.get('year')
  miles = request.args.get('miles')
  return get_unsold_cars(make, model, year, miles)

@app.route('/batch-create-cars/', methods=['POST'])
def batch_create_cars_api():
  return batch_create_cars()


'''Employee APIs'''
@app.route('/employees/', methods = ['GET'])
def get_employees_api():
  return get_employees()


'''Authentation APIs'''
@app.route('/login/', methods = ['POST'])
def login_api():
  return login()
  
@app.route('/logout/', methods = ['GET'])
def logout_api():
  return logout()

@app.route('/new-customer/', methods = ['POST'])
def create_new_customer_api():
  return create_new_customer()


'''Testing APIs'''
@app.route('/adminpage/', methods = ['GET'])
@user_middleware(['manager'])
def helloA():
  return "Hello admin!"

@app.route('/')
def hello():
  return "Shhh, ur not supposed to be here!"