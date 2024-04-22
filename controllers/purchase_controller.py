from flask import jsonify, request
from app import JWT_SECRETKEY
import jwt
from models.purchase import Purchase
from models.salesrep import SalesRep
from models.customer import Customer
from models.car import Car
from controllers.salesrep_controller import *
from controllers.customer_controller import *
from controllers.car_controller import *

from app import db

def format_purchase(purchase):
  
  salesrep = db.session.get(SalesRep, purchase.sales_rep_id);
  customer = db.session.get(Customer, purchase.customer_id);
  car = db.session.get(Car, purchase.car_id);

  return {
    "id": purchase.id,
    "customer_id": customer.id,
    "customer_username": customer.username,
    "customer_name" : customer.name,
    
    "sales_rep_id": salesrep.id,
    "sales_rep_username": salesrep.username,
    "sales_rep_name" : salesrep.name,
   
    "car_id": car.id,
    "car_vin" : car.vin,
    "car_make" : car.make,
    "car_model" : car.model,
    "car_year" : car.year,
    "car_imageUrl" : car.imageUrl,
    "car_price" : car.price,
    "car_miles" : car.miles,
    "car_description" : car.description,
    
    "time_purchased": purchase.time_purchased
  }
  
def create_purchase():
  data = request.json

  # Check for required fields
  for field in ['salesrep_id', 'car_id']:
    if field not in data:
      return jsonify({'error': f'Missing required field: {field}'}), 400
  
  token = request.cookies.get('auth')
  payload = jwt.decode(token, JWT_SECRETKEY, algorithms=['HS256'])
  customer_id = payload.get('userId')
  sales_rep_id = data.get('salesrep_id')
  car_id = data.get('car_id')
  
  customer = db.session.get(Customer, customer_id)
  if not customer:
    return jsonify({'error': 'Must be a customer'}), 404
  
  purchase = Purchase(sales_rep_id=sales_rep_id, customer_id=customer_id, car_id=car_id)
  db.session.add(purchase)

  try:
    db.session.commit()
    car = Car.query.get(car_id)
    car.is_sold = 'Y'
    db.session.commit()
    return format_purchase(purchase)
  
  except Exception as e:
    db.session.rollback()
    return jsonify({'error': 'Error in create_purchase()', 'details': str(e)}), 500
  finally:
    db.session.close()
    
def delete_purchase(id):
  purchase = db.session.get(Purchase, id)
  if not purchase:
    return jsonify({"error": "Purchase not found"}), 404
  try:
    db.session.delete(purchase)
    db.session.commit()
    return f'purchase (id: {id}) deleted!'
  except Exception as e:
    return jsonify({'error': 'Error in delete_purchase()', 'details': str(e)}), 500
  finally:
    db.session.close()
    
def get_purchase(id):
  purchase = db.session.get(Purchase, id)
  if not purchase:
    return jsonify({"error": "Purchase not found"}), 404

  return {'purchase': format_purchase(purchase)}

def update_purchase(id):
  purchase = db.session.get(Purchase, id)
  if not purchase:
    return jsonify({"error": "Purchase not found"}), 404

  data = request.json
  purchase.sales_rep_id = data.get('sales_rep_id', purchase.sales_rep_id)
  purchase.customer_id = data.get('customer_id', purchase.customer_id)
  purchase.car_id = data.get('car_id', purchase.car_id)

  try:
    db.session.commit()
    return {'Purchase': format(purchase)}
  except Exception as e:
    return jsonify({'error': 'Error in edit_purchase()', 'details': str(e)}), 500
  finally:
    db.session.close()
    
def get_purchases():
  purchases = Purchase.query.order_by(Purchase.time_purchased.asc()).all()
  purchases_list = []
  for purchase in purchases:
    purchases_list.append(format_purchase(purchase))
  return {'purchases': purchases_list}

def batch_create_purchases():
  purchases_data = request.json
  if not purchases_data:
    return jsonify({'error': 'purchase data not provided'}), 400
  purchases = []
  for purchases_info in purchases_data:
   
    sales_rep_id = purchases_info.get('sales_rep_id')
    customer_id = purchases_info.get('customer_id')
    car_id = purchases_info.get('car_id')
    purchase = Purchase(sales_rep_id=sales_rep_id, customer_id=customer_id, car_id=car_id)
    purchases.append(purchase)

  try:
    db.session.add_all(purchases)
    db.session.commit()
    return 'purchase added successfully'
  except Exception as e:
    db.session.rollback()
    return jsonify({'error': 'Failed to create batch purchase', 'details': str(e)}), 500
  finally:
    db.session.close()

def get_m_purchases():
  token = request.cookies.get('auth')
  payload = jwt.decode(token, JWT_SECRETKEY, algorithms=['HS256'])
  manager_id = payload.get('userId')
  
  sales_reps_managed = SalesRep.query.filter_by(manager_id=manager_id).all()
  sales_rep_ids = [sales_rep.id for sales_rep in sales_reps_managed]
  
  purchases = Purchase.query.filter(Purchase.sales_rep_id.in_(sales_rep_ids)).order_by(Purchase.time_purchased).all()
  
  return jsonify({'purchases': [format_purchase(purchase) for purchase in purchases]})

def get_m_purchases_total():
  token = request.cookies.get('auth')
  payload = jwt.decode(token, JWT_SECRETKEY, algorithms=['HS256'])
  manager_id = payload.get('userId')
  
  sales_reps_managed = SalesRep.query.filter_by(manager_id=manager_id).all()
  sales_rep_ids = [sales_rep.id for sales_rep in sales_reps_managed]
  
  purchases = Purchase.query.filter(Purchase.sales_rep_id.in_(sales_rep_ids)).order_by(Purchase.time_purchased).all()
  
  total = 0
  for purchase in purchases:
    car = db.session.get(Car, purchase.car_id);
    total += car.price
  
  return jsonify({'total_purchases': total})

def get_s_purchases():
  token = request.cookies.get('auth')
  payload = jwt.decode(token, JWT_SECRETKEY, algorithms=['HS256'])
  sale_rep_id = payload.get('userId')
  purchases = Purchase.query.filter_by(sales_rep_id=sale_rep_id).order_by(Purchase.time_purchased).all()
  return jsonify({'purchases': [format_purchase(purchase) for purchase in purchases]})

def get_s_purchases_total():
  token = request.cookies.get('auth')
  payload = jwt.decode(token, JWT_SECRETKEY, algorithms=['HS256'])
  sale_rep_id = payload.get('userId')
  purchases = Purchase.query.filter_by(sales_rep_id=sale_rep_id).order_by(Purchase.time_purchased).all()
  
  total = 0
  for purchase in purchases:
    car = db.session.get(Car, purchase.car_id);
    total += car.price
  
  return jsonify({'total_purchases': total})


def get_c_purchases():
  token = request.cookies.get('auth')
  payload = jwt.decode(token, JWT_SECRETKEY, algorithms=['HS256'])
  customer_id = payload.get('userId')
  purchases = Purchase.query.filter_by(customer_id=customer_id).order_by(Purchase.time_purchased).all()
  return jsonify({'purchases': [format_purchase(purchase) for purchase in purchases]})


