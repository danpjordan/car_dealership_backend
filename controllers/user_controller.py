from flask import jsonify, request
from models.user import User
from app import JWT_SECRETKEY
import jwt
import bcrypt

from app import app, db

def format_user(user):
  return {
    "id": user.id,
    "username": user.username,
    "name" : user.name,
    "role": user.role,
    "email": user.email,
    "phone": user.phone,
  }
  
def update_user():
  token = request.cookies.get('auth')
  payload = jwt.decode(token, JWT_SECRETKEY, algorithms=['HS256'])
  user_id = payload.get('userId')
  user = db.session.get(User, user_id)

  data = request.json
  user.username = data.get('username', user.username)
  user.name = data.get('name', user.name)
  user.email = data.get('email', user.email)
  user.phone = data.get('phone', user.phone)
  
  if data.get('password'):
    password = bcrypt.hashpw(data.get('password').encode('utf-8'), 
                    bcrypt.gensalt()).decode('utf-8')
    user.password = password
    
  try:
    db.session.commit()
    return {'User': format_user(user)}
  except Exception as e:
    return jsonify({'error': 'Error in update_user()', 'details': str(e)}), 500
  finally:
    db.session.close()
    
def deactivate_user():
  token = request.cookies.get('auth')
  payload = jwt.decode(token, JWT_SECRETKEY, algorithms=['HS256'])
  user_id = payload.get('userId')
  user = db.session.get(User, user_id)

  user.active_status = 'N'
    
  try:
    db.session.commit()
    return {'Deactivated user': format_user(user)}
  except Exception as e:
    return jsonify({'error': 'Error in deactivate_user()', 'details': str(e)}), 500
  finally:
    db.session.close()
    
def get_user():
  token = request.cookies.get('auth')
  payload = jwt.decode(token, JWT_SECRETKEY, algorithms=['HS256'])
  user_id = payload.get('userId')
  user = db.session.get(User, user_id)
  
  if user is None:
    return jsonify({'error': 'Manager not found'}), 404
  return jsonify(format_user(user))

