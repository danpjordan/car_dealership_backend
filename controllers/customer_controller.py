from flask import jsonify, request
from models.customer import Customer
from app import app, db

def format_customer(customer):
  return {
    "id": customer.id,
    "username": customer.username,
    "name" : customer.name,
    "email": customer.email,
    "phone": customer.phone,
  }

def create_customer():
  data = request.json
  if ('username') not in data:
    return jsonify({'error': 'username not provided'}), 400
  
  if ('password') not in data:
    return jsonify({'error': 'password not provided'}), 400
  
  name = data.get('name')
  username = data.get('username')
  password = data.get('password')
  email = data.get('email')
  phone = data.get('phone')
  usr_id = data.get('usr_id')
  active_status = data.get('active_status')
  
  customer = Customer(name=name, username=username, password=password, email=email, phone=phone, active_status=active_status, usr_id=usr_id)
  db.session.add(customer)
  
  try:
    db.session.commit()
    return format_customer(customer)
  except Exception as e:
    db.session.rollback()
    return jsonify({'error': 'Error in create_customer()', 'details': str(e)}), 500
  finally:
    db.session.close()

def delete_customer(id):
  customer = db.session.get(Customer, id)
  if not customer:
    return jsonify({"error": "Customer not found"}), 404
  try:
    db.session.delete(customer)
    db.session.commit()
    return f'Customer (id: {id}) deleted!'
  except Exception as e:
    return jsonify({'error': 'Error in delete_customer()', 'details': str(e)}), 500
  finally:
    db.session.close()

def get_customer(id):
  customer = db.session.get(Customer, id)
  if not customer:
    return jsonify({"error": "Customer not found"}), 404
  return format_customer(customer)

def get_customers():
  customers = Customer.query.order_by(Customer.timeCreated).all()
  return jsonify([format_customer(customer) for customer in customers])

def batch_create_customers():
  data = request.json
  if not data:
    return jsonify({'error': 'No data provided'}), 400
  customers = []
  for customer_info in data:
    name = customer_info.get('name')
    username = customer_info.get('username')
    password = customer_info.get('password')
    email = customer_info.get('email')
    phone = customer_info.get('phone')
    usr_id = customer_info.get('usr_id')
    active_status = customer_info.get('active_status')
    
    customer = Customer(name=name, username=username, password=password, email=email, phone=phone, usr_id=usr_id, active_status=active_status)
    customers.append(customer)
  try:
    db.session.add_all(customers)
    db.session.commit()
    return "Customers created!"
  except Exception as e: 
    db.session.rollback()
    return jsonify({'error': 'Error in batch_create_customers()', 'details': str(e)}), 500
  finally:
    db.session.close()

def get_m_customer():
  customers = Customer.query.order_by(Customer.timeCreated).all()
  return jsonify({'costomers': [format_customer(customer) for customer in customers]})

def get_s_customer():
  with app.app_context():
    salesrep_customer_view = db.Table('salesrep_customer_view', db.MetaData(), autoload_with=db.engine)
  salesreps = db.session.query(salesrep_customer_view).order_by(salesrep_customer_view.c.timeCreated.asc()).all()

  return jsonify({'costomers': [format_customer(salesrep) for salesrep in salesreps]})
