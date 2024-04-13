from flask import jsonify, request
from models.customer import Customer
from app import db

def format_customer(customer):
  return {
    "id": customer.id,
    "username": customer.username,
    "name" : customer.name,
    "email": customer.email,
    "phone": customer.phone,
    "cars_purchased": customer.cars_purchased
  }

def create_customer():
  data = request.json
  if ('name') not in data:
    return jsonify({'error': 'name not provided'}), 400
  
  if ('username') not in data:
    return jsonify({'error': 'username not provided'}), 400
  
  if ('password') not in data:
    return jsonify({'error': 'password not provided'}), 400
  
  if ('email') not in data:
    return jsonify({'error': 'email not provided'}), 400
  
  if ('phone') not in data:
    return jsonify({'error': 'phone not provided'}), 400
  
  name = data.get('name')
  username = data.get('username')
  password = data.get('password')
  email = data.get('email')
  phone = data.get('phone')
  
  customer = Customer(name, username, password, email, phone)
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

def update_customer(id):
  customer = db.session.get(Customer, id)
  if not customer:
    return jsonify({"error": "Customer not found"}), 404
  
  data = request.json
  if ('name') in data:
    customer.name = data.get('name')
  if ('email') in data:
    customer.email = data.get('email')
  if ('phone') in data:
    customer.phone = data.get('phone')
  if ('cars_purchased') in data:
    customer.cars_purchased = data.get('cars_purchased')
  
  try:
    db.session.commit()
    return format_customer(customer)
  except Exception as e:
    db.session.rollback()
    return jsonify({'error': 'Error in update_customer()', 'details': str(e)}), 500
  finally:
    db.session.close()

def get_customers():
  customers = Customer.query.all()
  return jsonify([format_customer(customer) for customer in customers])

def batch_create_customers():
  data = request.json
  if not data:
    return jsonify({'error': 'No data provided'}), 400
  customers = []
  for customer in data:
    name = customer.get('name')
    username = customer.get('username')
    password = customer.get('password')
    email = customer.get('email')
    phone = customer.get('phone')
    
    customer = Customer(name, username, password, email, phone)
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