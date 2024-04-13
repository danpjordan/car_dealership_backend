from flask import request, jsonify
from app import db
from models.manager import Manager

def format_manager(manager): 
  return {
    "id": manager.id,
    "username": manager.username,
    "name" : manager.name,
    "emp_role": manager.emp_role,
    "imageUrl": manager.imageUrl,
    "xUrl": manager.xUrl,
    "linkedinUrl": manager.linkedinUrl
  }

def create_manager():
  data = request.json
  if ('name') not in data:
    return jsonify({'error': 'name not provided'}), 400
  
  if ('username') not in data:
    return jsonify({'error': 'username not provided'}), 400
  
  if ('password') not in data:
    return jsonify({'error': 'password not provided'}), 400
  
  name = data.get('name')
  username = data.get('username')
  password = data.get('password')
  emp_role = data.get('emp_role')
  imageUrl = data.get('imageUrl')
  xUrl = data.get('xUrl')
  linkedinUrl = data.get('linkedinUrl')
  
  manager = Manager(name, username, password, emp_role, imageUrl, xUrl, linkedinUrl)
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
  manager = db.session.get(Manager, id)
  if not manager:
    return jsonify({"error": "Manager not found"}), 404
  try:
    db.session.delete(manager)
    db.session.commit()
    return f'Manager (id: {id}) deleted!'
  except Exception as e:
    return jsonify({'error': 'Error in delete_manager()', 'details': str(e)}), 500
  finally:
    db.session.close()

def get_manager(id):
  manager = db.session.get(Manager, id)
  if not manager:
    return jsonify({"error": "Manager not found"}), 404
  return format_manager(manager)

def update_manager(id):
  manager = db.session.get(Manager, id)
  if not manager:
    return jsonify({"error": "Manager not found"}), 404

  data = request.json
  manager.name = data.get('name', manager.name)
  manager.username = data.get('username', manager.username)
  manager.password = data.get('password', manager.password)
  manager.emp_role = data.get('emp_role', manager.emp_role)
  manager.imageUrl = data.get('imageUrl', manager.imageUrl)
  manager.xUrl = data.get('xUrl', manager.xUrl)
  manager.linkedinUrl = data.get('linkedinUrl', manager.linkedinUrl)
  
  try:
    db.session.commit()
    return format_manager(manager)
  except Exception as e:
    db.session.rollback()
    return jsonify({'error': 'Error in update_manager()', 'details': str(e)}), 500
  finally:
    db.session.close()

def get_managers():
  managers = db.session.query(Manager).all()
  return {'managers': [format_manager(manager) for manager in managers]}

def batch_create_managers():
  data = request.json
  managers = []
  for manager in data:
    name = manager.get('name')
    username = manager.get('username')
    password = manager.get('password')
    emp_role = manager.get('emp_role')
    imageUrl = manager.get('imageUrl')
    xUrl = manager.get('xUrl')
    linkedinUrl = manager.get('linkedinUrl')
    managers.append(Manager(name, username, password, emp_role, imageUrl, xUrl, linkedinUrl))