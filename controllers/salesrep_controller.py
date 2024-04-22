from flask import jsonify, request
from models.salesrep import SalesRep
from app import app, db


def format_salesrep(salesrep):
  return {
    "id": salesrep.id,
    "manager_id": salesrep.manager_id,
    "username": salesrep.username,
    "name" : salesrep.name,
    "role": salesrep.role,
    "email": salesrep.email,
    "phone": salesrep.phone,
    "imageUrl": salesrep.imageUrl,
    "xUrl": salesrep.xUrl,
    "linkedinUrl": salesrep.linkedinUrl,
    "salary": salesrep.salary
  }

def format_salesrep_for_manager(salesrep):
  return {
    "id": salesrep.id,
    "username": salesrep.username,
    "name" : salesrep.name,
    "email": salesrep.email,
    "phone": salesrep.phone,
    "manager_name" : salesrep.manager_name,
    "salary" : salesrep.salary 
  }

def create_salesrep():
  data = request.json
  
  # Check for required fields
  for field in ['name', 'username', 'password', 'manager_id']:
    if field not in data:
      return jsonify({'error': f'Missing required field: {field}'}), 400
    
  name = data.get('name')
  manager_id = data.get('manager_id')
  username = data.get('username')
  password = data.get('password')
  imageUrl = data.get('imageUrl')
  xUrl = data.get('xUrl')
  email = data.get('email')
  phone = data.get('phone')
  linkedinUrl = data.get('linkedinUrl')
  usr_id = data.get('usr_id')
  active_status=data.get('active_status')
  salary = data.get('salary')

  salesrep = SalesRep(username=username, password=password, name=name, email=email, phone=phone, manager_id=manager_id, imageUrl=imageUrl, xUrl=xUrl, linkedinUrl=linkedinUrl, salary=salary, active_status=active_status, usr_id=usr_id)
  db.session.add(salesrep)
  
  try:
    db.session.commit()
    return format_salesrep(salesrep)
  except Exception as e:
    db.session.rollback()
    return jsonify({'error': 'Error in create_salesrep()', 'details': str(e)}), 500
  finally:
    db.session.close()

# def delete_salesrep(id):
#   salesrep = SalesRep.query.get(id)
#   if not salesrep:
#     return jsonify({"error": "SalesRep not found"}), 404
#   try:
#     db.session.delete(salesrep)
#     db.session.commit()
#     return f'SalesRep (id: {id}) deleted!'
#   except Exception as e:
#     return jsonify({'error': 'Error in delete_salesrep()', 'details': str(e)}), 500
#   finally:
#     db.session.close()

# def update_salesrep(id):
#   salesrep = SalesRep.query.get(id)
#   if not salesrep:
#     return jsonify({"error": "SalesRep not found"}), 404
  
#   data = request.json
#   salesrep.imageUrl = data.get('imageUrl', salesrep.imageUrl)
#   salesrep.xUrl = data.get('xUrl', salesrep.xUrl)
#   salesrep.linkedinUrl = data.get('linkedinUrl', salesrep.linkedinUrl)
#   salesrep.manager_id = data.get('manager_id', salesrep.manager_id)
#   salesrep.salary = data.get('salary', salesrep.salary)
  
#   try:
#     db.session.commit()
#     return format_salesrep(salesrep)
#   except Exception as e:
#     db.session.rollback()
#     return jsonify({'error': 'Error in update_salesrep()', 'details': str(e)}), 500
#   finally:
    db.session.close()

# def get_salesrep(id):
  # salesrep = SalesRep.query.get(id)
  # if not salesrep:
  #   return jsonify({'error': 'SalesRep not found'}), 404
  # return jsonify(format_salesrep(salesrep))

def get_salesreps():
  salesreps = SalesRep.query.filter(SalesRep.active_status == 'Y').order_by(SalesRep.timeCreated).all()
  return jsonify([format_salesrep(salesrep) for salesrep in salesreps])

def batch_create_salesreps():
  salesrep_data = request.json
  if not salesrep_data:
    return jsonify({'error': 'No data provided'}), 400
  salesreps = []
  for salesrep_info in salesrep_data:
    salesrep = SalesRep(
      name=salesrep_info.get('name'),
      usr_id=salesrep_info.get('usr_id'),
      manager_id = salesrep_info.get('manager_id'),
      username=salesrep_info.get('username'),
      password=salesrep_info.get('password'),
      imageUrl=salesrep_info.get('imageUrl'),
      xUrl=salesrep_info.get('xUrl'),
      linkedinUrl=salesrep_info.get('linkedinUrl'),
      phone = salesrep_info.get('phone'),
      email = salesrep_info.get('email'),
      salary= salesrep_info.get('salary'),
      active_status=salesrep_info.get('active_status')
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

def get_m_salesreps():
  with app.app_context():
    manager_salesrep_view = db.Table('manager_salesrep_view', db.MetaData(), autoload_with=db.engine)
  salesreps = db.session.query(manager_salesrep_view).order_by(manager_salesrep_view.c.timeCreated.asc()).all()
  return jsonify({'salesreps': [format_salesrep_for_manager(salesrep) for salesrep in salesreps]})

