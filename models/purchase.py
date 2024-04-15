from app import db
import random
from datetime import datetime

class Purchase(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  sales_rep_id = db.Column(db.Integer, db.ForeignKey('sales_rep.id'), nullable=False)
  customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
  car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False, unique=True)
  time_purchased = db.Column(db.DateTime, nullable=False)

  def __init__(self, sales_rep_id=sales_rep_id, customer_id=customer_id, car_id=car_id):
    self.id = self.generate_unique_id()
    self.sales_rep_id = sales_rep_id
    self.customer_id = customer_id
    self.car_id = car_id
    self.time_purchased = datetime.utcnow()
              
  def generate_unique_id(self):
    while True:
      random_id = random.randint(10000, 99999)
      is_purchase = Purchase.query.filter_by(id=random_id).first()
      if not is_purchase:
        return random_id