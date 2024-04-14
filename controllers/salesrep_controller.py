from flask import jsonify, request
from models.salesrep import SalesRep
from app import db


def format_salesrep(salesrep):
  return {
    "id": salesrep.id,
    "username": salesrep.username,
    "name" : salesrep.name,
    "emp_role": salesrep.emp_role,
    "imageUrl": salesrep.imageUrl,
    "xUrl": salesrep.xUrl,
    "linkedinUrl": salesrep.linkedinUrl,
    "number_of_sales": salesrep.number_of_sales
  }

def create_salesrep():
  data = request.json
  
  # Check for required fields
  for field in ['name', 'username', 'password']:
    if field not in data:
      return jsonify({'error': f'Missing required field: {field}'}), 400
    
  name = data.get('name')
  username = data.get('username')
  password = data.get('password')
  imageUrl = data.get('imageUrl')
  xUrl = data.get('xUrl')
  linkedinUrl = data.get('linkedinUrl')
  number_of_sales = data.get('number_of_sales')

  salesrep = SalesRep(name=name, username=username, password=password, imageUrl=imageUrl, xUrl=xUrl, linkedinUrl=linkedinUrl, number_of_sales=number_of_sales)
  db.session.add(salesrep)
  
  try:
    db.session.commit()
    return format_salesrep(salesrep)
  except Exception as e:
    db.session.rollback()
    return jsonify({'error': 'Error in create_salesrep()', 'details': str(e)}), 500
  finally:
    db.session.close()

def delete_salesrep(id):
  salesrep = SalesRep.query.get(id)
  if not salesrep:
    return jsonify({"error": "SalesRep not found"}), 404
  try:
    db.session.delete(salesrep)
    db.session.commit()
    return f'SalesRep (id: {id}) deleted!'
  except Exception as e:
    return jsonify({'error': 'Error in delete_salesrep()', 'details': str(e)}), 500
  finally:
    db.session.close()

def update_salesrep(id):
  salesrep = SalesRep.query.get(id)
  if not salesrep:
    return jsonify({"error": "SalesRep not found"}), 404
  
  data = request.json
  salesrep.name = data.get('name', salesrep.name)
  salesrep.username = data.get('username', salesrep.username)
  salesrep.password = data.get('password', salesrep.password)
  salesrep.imageUrl = data.get('imageUrl', salesrep.imageUrl)
  salesrep.xUrl = data.get('xUrl', salesrep.xUrl)
  salesrep.linkedinUrl = data.get('linkedinUrl', salesrep.linkedinUrl)
  salesrep.number_of_sales = data.get('number_of_sales', salesrep.number_of_sales)

  try:
    db.session.commit()
    return format_salesrep(salesrep)
  except Exception as e:
    db.session.rollback()
    return jsonify({'error': 'Error in update_salesrep()', 'details': str(e)}), 500
  finally:
    db.session.close()
  
def get_salesrep(id):
  salesrep = SalesRep.query.get(id)
  if not salesrep:
    return jsonify({'error': 'SalesRep not found'}), 404
  return jsonify(format_salesrep(salesrep))

def get_all_salesreps():
  salesreps = SalesRep.query.all()
  return jsonify([format_salesrep(salesrep) for salesrep in salesreps])

def batch_create_salesreps():
  salesrep_data = request.json
  if not salesrep_data:
    return jsonify({'error': 'No data provided'}), 400
  salesreps = []
  for salesrep_info in salesrep_data:
    salesrep = SalesRep(
      name=salesrep_info.get('name'),
      username=salesrep_info.get('username'),
      password=salesrep_info.get('password'),
      imageUrl=salesrep_info.get('imageUrl'),
      xUrl=salesrep_info.get('xUrl'),
      linkedinUrl=salesrep_info.get('linkedinUrl'),
      number_of_sales=salesrep_info.get('number_of_sales')
    )
    salesreps.append(salesrep)
  
  try:
    db.session.add_all(salesreps)
    db.session.commit()
    return jsonify({'message': 'SalesReps created successfully'})
  except Exception as e:
    db.session.rollback()
    return jsonify({'error': 'Error in batch_create_salesreps()', 'details': str(e)}), 500
  finally:
    db.session.close()


