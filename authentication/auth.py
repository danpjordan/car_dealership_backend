from flask import jsonify, make_response, request
from app import JWT_SECRETKEY
import jwt
from functools import wraps
from datetime import datetime, timedelta

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
  response = make_response({'status':True, 'msg':'Login successful'})
  response.set_cookie('auth', token)
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
            print(token)
            if not token:
                return jsonify({'error': 'Access failed (missing token)'}), 200
            try:
                payload = jwt.decode(token, JWT_SECRETKEY, algorithms=['HS256'])
                print(payload)
                print(payload.get('role'))
                if payload.get('role') not in roles:
                    return jsonify({'error': 'Access failed (requires admin)'}), 200
            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Access failed (unauthorized signature)'}), 200
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Access failed (invalid token)'}), 200
            return func()
        return wrapper
    return decorator
