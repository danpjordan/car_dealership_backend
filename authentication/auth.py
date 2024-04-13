from flask import jsonify, make_response, request
from app import JWT_SECRETKEY
import jwt
from functools import wraps
from datetime import datetime, timedelta
from models.user import *

def createToken(user):
  token = jwt.encode(
    payload={
        'userId':user.id,
        'username':user.username,
        'exp':datetime.utcnow() + timedelta(minutes=60),
        'role':user.role
    },
        key=JWT_SECRETKEY, algorithm='HS256')
  return token

def setCookie(token):
    response = make_response({'status': True, 'msg': 'Login successful'})
    response.set_cookie('auth', token, max_age=60*60)
    return response
  
def removeCookie():
  responce = make_response({'status':True, 'msg':'Logout successful'})
  responce.delete_cookie('auth')
  return responce

def user_middleware(roles):
    def decorator(func):
        @wraps(func)
        def wrapper():
            token = request.cookies.get('auth')
            if not token:
                return jsonify({'error': 'Access failed (missing token)'}), 200
            try:
                payload = jwt.decode(token, JWT_SECRETKEY, algorithms=['HS256'])
                if payload.get('role') not in roles:
                    return jsonify({'error': 'Access failed (requires admin)'}), 200
            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Access failed (unauthorized signature)'}), 200
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Access failed (invalid token)'}), 200
            return func()
        return wrapper
    return decorator


def login():
  user=None
  try:
    username = request.json.get('username')
    user=User.query.filter(
        User.username==username,
        User.active_status=='Y'
        ).first()
    if not user:
      return jsonify({'error': 'user not found'}, 200)
    if not bcrypt.checkpw(
      request.json.get('password').encode('utf-8'),
      user.password.encode('utf-8')
    ):
      return jsonify({'error': 'invalid password'}, 200)
    
  except Exception as e:
    return jsonify({'error': 'unsuccessful login', 'details': str(e)}), 400
  
  try:
    token = createToken(user)
    print(setCookie(token))
    print(format_user(user))
    return setCookie(token), format_user(user)
  except Exception as e:
    return jsonify({'error': 'failed to create token', 'details': str(e)}), 400

def logout():
  try:
    return removeCookie()

  except Exception as e:
    return jsonify({'error': 'logout unsuccessful', 'details': str(e)}), 400

def create_user():
  data = request.json
  if ('username') not in data:
    return jsonify({'error': 'username not provided'}), 400
  if ('password') not in data:
    return jsonify({'error': 'password not provided'}), 400
   
  username = data.get('username')
  role = data.get('role')
  password = data.get('password')
  user = User(username, password, role)
  
  db.session.add(user)

  try:
    db.session.commit()
    return format_user(user)
  except Exception as e:
    db.session.rollback()
    return jsonify({'error': 'Error in create_employee()', 'details': str(e)}), 500
  finally:
    db.session.close()
