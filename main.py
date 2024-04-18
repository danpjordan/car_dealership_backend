from app import db
from api import *

if __name__ == '__main__':
  with app.app_context():
    db.create_all()
    
  app.run(port=8000)
