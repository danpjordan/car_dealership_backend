from flask import jsonify, request
from models.manager import Manager
from app import db

def format_manager(manager): 
  return {
    "id": manager.id,
    "username": manager.username,
    "name" : manager.name,
    "role": manager.role,
    "imageUrl": manager.imageUrl,
    "xUrl": manager.xUrl,
    "linkedinUrl": manager.linkedinUrl,
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
  xUrl = data.get('xUrl')
  linkedinUrl = data.get('linkedinUrl')
  usr_id = data.get('usr_id')

  manager = Manager(name, username, password, imageUrl, xUrl, linkedinUrl, usr_id)
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

def update_manager(id):
  manager = Manager.query.get(id)
  if manager is None:
    return jsonify({'error': 'Manager not found'}), 404
  
  data = request.json
  if 'name' in data:
    manager.name = data.get('name', manager.name)
  if 'username' in data:
    manager.username = data.get('username', manager.username)
  if 'password' in data:
    manager.password = data.get('password', manager.password)
  if 'imageUrl' in data:
    manager.imageUrl = data.get('imageUrl', manager.imageUrl)
  if 'xUrl' in data:
    manager.xUrl = data.get('xUrl', manager.xUrl)
  if 'linkedinUrl' in data:
    manager.linkedinUrl = data.get('linkedinUrl', manager.linkedinUrl)
  
  try:
    db.session.commit()
    return jsonify(format_manager(manager))
  except Exception as e:
    db.session.rollback()
    return jsonify({'error': 'Error in update_manager()', 'details': str(e)}), 500
  finally:
    db.session.close()

def get_managers():
  managers = Manager.query.order_by(Manager.timeCreated).all()
  return jsonify({'managers': [format_manager(manager) for manager in managers]})
  
  # employees = Employee.query.order_by(Employee.timeCreated).all()
  # employees_list = []
  # for employee in employees:
  #   employees_list.append(format_employee(employee))
  # return {'employees': employees_list}

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
    xUrl = manager_info.get('xUrl')
    linkedinUrl = manager_info.get('linkedinUrl')
    usr_id = manager_info.get('usr_id')

    manager = Manager(name, username, password, imageUrl, xUrl, linkedinUrl, usr_id)
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
