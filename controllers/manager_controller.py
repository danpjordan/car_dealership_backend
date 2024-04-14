from flask import jsonify, request
from models.manager import Manager
from app import db


def format_manager(manager): 
  return {
    "id": manager.id,
    "username": manager.username,
    "name" : manager.name,
    "emp_role": manager.emp_role,
    "imageUrl": manager.imageUrl,
    "xUrl": manager.xUrl,
    "linkedinUrl": manager.linkedinUrl,
    "people_managed": manager.people_managed
  }

def create_manager():
  data = request.json
  if 'name' not in data:
    return jsonify({'error': 'name not provided'}), 400
  if 'username' not in data:
    return jsonify({'error': 'username not provided'}), 400
  if 'password' not in data:
    return jsonify({'error': 'password not provided'}), 400
  if 'emp_role' not in data:
    return jsonify({'error': 'emp_role not provided'}), 400
  
  name = data.get('name')
  username = data.get('username')
  password = data.get('password')
  emp_role = data.get('emp_role')
  imageUrl = data.get('imageUrl')
  xUrl = data.get('xUrl')
  linkedinUrl = data.get('linkedinUrl')
  people_managed = data.get('people_managed', 0)

  manager = Manager(name, username, password, emp_role, imageUrl, xUrl, linkedinUrl, people_managed)
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
  if 'emp_role' in data:
    manager.emp_role = data.get('emp_role', manager.emp_role)
  if 'imageUrl' in data:
    manager.imageUrl = data.get('imageUrl', manager.imageUrl)
  if 'xUrl' in data:
    manager.xUrl = data.get('xUrl', manager.xUrl)
  if 'linkedinUrl' in data:
    manager.linkedinUrl = data.get('linkedinUrl', manager.linkedinUrl)
  if 'people_managed' in data:
    manager.people_managed = data.get('people_managed', manager.people_managed)
  
  try:
    db.session.commit()
    return jsonify(format_manager(manager))
  except Exception as e:
    db.session.rollback()
    return jsonify({'error': 'Error in update_manager()', 'details': str(e)}), 500
  finally:
    db.session.close()

def get_managers():
  managers = Manager.query.all()
  return jsonify({'managers': [format_manager(manager) for manager in managers]})

def batch_create_managers():
  data = request.json
  if 'managers' not in data:
    return jsonify({'error': 'managers not provided'}), 400
  
  managers = data.get('managers')

  for manager in managers:
    name = manager.get('name')
    username = manager.get('username')
    password = manager.get('password')
    emp_role = manager.get('emp_role')
    imageUrl = manager.get('imageUrl')
    xUrl = manager.get('xUrl')
    linkedinUrl = manager.get('linkedinUrl')
    people_managed = manager.get('people_managed', 0)

    manager = Manager(name, username, password, emp_role, imageUrl, xUrl, linkedinUrl, people_managed)
    db.session.add(manager)
  
  try:
    db.session.commit()
    return jsonify({'success': 'Managers created'})
  except Exception as e:
    db.session.rollback()
    return jsonify({'error': 'Error in batch_create_managers()', 'details': str(e)}), 500
  finally:
    db.session.close()
