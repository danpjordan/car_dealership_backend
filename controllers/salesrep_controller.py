from flask import jsonify, request
from models.salesrep import SalesRep
from app import db

def format_salesrep(salesrep):
  return {
    "id": salesrep.id,
    "username": salesrep.username,
    "name" : salesrep.name,
    "imageUrl": salesrep.imageUrl,
    "xUrl": salesrep.xUrl,
    "linkedinUrl": salesrep.linkedinUrl
  }

def create_salesrep():
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
  imageUrl = data.get('imageUrl')
  xUrl = data.get('xUrl')
  linkedinUrl = data.get('linkedinUrl')
  
  salesrep = SalesRep(name, username, password, imageUrl, xUrl, linkedinUrl)
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
  salesrep = db.session.get(SalesRep, id)
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

def get_salesrep(id):
  salesrep = db.session.get(SalesRep, id)
  if not salesrep:
    return jsonify({"error": "SalesRep not found"}), 404
  return format_salesrep(salesrep)

def update_salesrep(id):
  salesrep = db.session.get(SalesRep, id)
  if not salesrep:
    return jsonify({"error": "SalesRep not found"}), 404

  data = request.json
  salesrep.name = data.get('name', salesrep.name)
  salesrep.username = data.get('username', salesrep.username)
  salesrep.imageUrl = data.get('imageUrl', salesrep.imageUrl)
  salesrep.xUrl = data.get('xUrl', salesrep.xUrl)
  salesrep.linkedinUrl = data.get('linkedinUrl', salesrep.linkedinUrl)
  
  try:
    db.session.commit()
    return format_salesrep(salesrep)
  except Exception as e:
    db.session.rollback()
    return jsonify({'error': 'Error in update_salesrep()', 'details': str(e)}), 500
  finally:
    db.session.close()

def get_salesreps():
  salesreps = db.session.query(SalesRep).all()
  return jsonify({'salesreps': [format_salesrep(salesrep) for salesrep in salesreps]})