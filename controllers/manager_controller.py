from flask import jsonify, request
from models.manager import Manager
from app import db

def format_manager(manager): 
  return {
    "id": manager.id,
    "username": manager.username,
    "name" : manager.name,
    "phone" : manager.phone,
    "email" : manager.email,
    "role": manager.role,
    "imageUrl": manager.imageUrl,
    "xUrl": manager.xUrl,
    "linkedinUrl": manager.linkedinUrl,
    "salary":manager.salary
  }

def create_manager():
  data = request.json
  if 'name' not in data:
    return jsonify({'error': 'name not provided'}), 400
  if 'username' not in data:
    return jsonify({'error': 'username not provided'}), 400
  if 'password' not in data:
    return jsonify({'error': 'password not provided'}), 400
  
  name = data.get('name')
  username = data.get('username')
  password = data.get('password')
  imageUrl = data.get('imageUrl')
  phone = data.get('phone')
  email = data.get('email')
  xUrl = data.get('xUrl')
  linkedinUrl = data.get('linkedinUrl')
  salary = data.get('salary')
  active_status = data.get('active_status')
  usr_id = data.get('usr_id')

  manager = Manager(username=username, password=password, name=name, email=email, phone=phone, imageUrl=imageUrl, xUrl=xUrl, linkedinUrl=linkedinUrl, salary=salary, active_status=active_status, usr_id=usr_id)
  db.session.add(manager)

  try:
    db.session.commit()
    return format_manager(manager)
  except Exception as e:
    db.session.rollback()
    return jsonify({'error': 'Error in create_manager()', 'details': str(e)}), 500
  finally:
    db.session.close()

def delete_manager(id):
  manager = Manager.query.get(id)
  if manager is None:
    return jsonify({'error': 'Manager not found'}), 404
  db.session.delete(manager)
  try:
    db.session.commit()
    return jsonify({'success': 'Manager deleted'})
  except Exception as e:
    db.session.rollback()
    return jsonify({'error': 'Error in delete_manager()', 'details': str(e)}), 500
  finally:
    db.session.close()

def get_manager(id):
  manager = Manager.query.get(id)
  if manager is None:
    return jsonify({'error': 'Manager not found'}), 404
  return jsonify(format_manager(manager))

def get_managers():
  managers = Manager.query.order_by(Manager.timeCreated).all()
  return jsonify({'managers': [format_manager(manager) for manager in managers]})

def batch_create_managers():
  manager_data = request.json
  if not manager_data:
    return jsonify({'error': 'managers not provided'}), 400
  
  managers = []

  for manager_info in manager_data:
    name = manager_info.get('name')
    username = manager_info.get('username')
    password = manager_info.get('password')
    imageUrl = manager_info.get('imageUrl')
    email = manager_info.get('email')
    phone = manager_info.get('phone')
    xUrl = manager_info.get('xUrl')
    linkedinUrl = manager_info.get('linkedinUrl')
    salary = manager_info.get('salary')
    active_status = manager_info.get('active_status')
    usr_id = manager_info.get('usr_id')
    

    manager = Manager(username=username, password=password, name=name, email=email, phone=phone, imageUrl=imageUrl, xUrl=xUrl, linkedinUrl=linkedinUrl, salary=salary, active_status=active_status, usr_id=usr_id)
    managers.append(manager)
  
  try:
    db.session.add_all(managers)
    db.session.commit()
    return 'managers added successfully'
  except Exception as e:
    db.session.rollback()
    return jsonify({'error': 'Error in batch_create_managers()', 'details': str(e)}), 500
  finally:
    db.session.close()
