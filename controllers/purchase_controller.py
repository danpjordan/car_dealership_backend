from flask import jsonify, request
from models.purchase import Purchase
from app import db


def format_purchase(purchase):
  return {
    "id": purchase.id,
    "sales_rep_id": purchase.sales_rep_id,
    "customer_id": purchase.customer_id,
    "car_id": purchase.car_id,
    "time_purchased": purchase.time_purchased
  }
  
def create_purchase():
  data = request.json

  # Check for required fields
  for field in ['salesrep_id', 'customer_id', 'car_id']:
    if field not in data:
      return jsonify({'error': f'Missing required field: {field}'}), 400
  
  sales_rep_id = data.get('sales_rep_id')
  customer_id = data.get('customer_id')
  car_id = data.get('car_id')
  
  purchase = Purchase(sales_rep_id=sales_rep_id, customer_id=customer_id, car_id=car_id)
  db.session.add(purchase)
  
  try:
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
  purchases = Purchase.query.order_by(purchases.timeCreated.asc()).all()
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
