from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

POSTGRES={
    'user':'postgres',
    'pw':'6569',
    'db':'car-dealership',
    'host':'localhost',
    'port':'5433'
}

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s'%POSTGRES
db = SQLAlchemy(app)
CORS(app)

if __name__ == '__main__':
  with app.app_context():
    db.create_all()
  app.run(port=8000)
