from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import bcrypt

JWT_SECRETKEY=bcrypt.hashpw(b'sUperKew1Se(rEtk3y', bcrypt.gensalt())

app = Flask(__name__)

POSTGRES={
  'user':'shoh',
  'pw':'java',
  'db':'car_dealership',
  'host':'localhost',
  'port':'5432' 
}

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s'%POSTGRES
db = SQLAlchemy(app)
CORS(app, supports_credentials=True, origins=['http://localhost:3000'])
