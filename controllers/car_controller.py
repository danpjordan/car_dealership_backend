from flask import jsonify, request
from models.car import Car
from app import app, db

def format_car(car):
  return {
    "id" : car.id,
    "vin" : car.vin,
    "make" : car.make,
    "model" : car.model,
    "year" : car.year,
    "imageUrl" : car.imageUrl,
    "price" : car.price,
    "miles" : car.miles,
    "description" : car.description,
    "timeCreated" : car.timeCreated
  }
  
def create_car():
  data = request.json
  if ('vin') not in data:
    return jsonify({'error': 'vin attribute not provided'}), 400
  
  vin = data.get('vin')
  make = data.get('make')
  model = data.get('model')
  year = data.get('year')
  imageUrl = data.get('imageUrl')
  price = data.get('price')
  miles = data.get('miles')
  description = data.get('description')
  car_id = data.get('car_id')
  is_sold = data.get('is_sold')
  
  
  car = Car(vin, make, model, year, imageUrl, price, miles, description, car_id, is_sold)
  db.session.add(car)
  
  try:
    db.session.commit()
    return format_car(car)
  except Exception as e:
    db.session.rollback()
    return jsonify({'error': 'Error in create_car()', 'details': str(e)}), 500
  finally:
    db.session.close()
    
def delete_car(id):
  car = db.session.get(Car, id)
  if not car:
    return jsonify({"error": "Car not found"}), 404
  try:
    db.session.delete(car)
    db.session.commit()
    return f'Car (id: {id}) deleted!'
  except Exception as e:
    return jsonify({'error': 'Error in delete_car()', 'details': str(e)}), 500
  finally:
    db.session.close()
    
def get_car(id):
  car = db.session.get(Car, id)
  if not car:
    return jsonify({"error": "Car not found"}), 404

  return {'car': format_car(car)}

def update_car(id):
  car = db.session.get(Car, id)
  if not car:
    return jsonify({"error": "Car not found"}), 404

  data = request.json
  car.vin = data.get('vin', car.vin)
  car.make = data.get('make', car.make)
  car.model = data.get('model', car.model)
  car.year = data.get('year', car.year)
  car.imageUrl = data.get('imageUrl', car.imageUrl)
  car.price = data.get('price', car.price)
  car.miles = data.get('miles', car.miles)
  car.description = data.get('description', car.description)
  car.is_sold = data.get('is_sold', car.is_sold)

  try:
    db.session.commit()
    return {'Car': format(car)}
  except Exception as e:
    return jsonify({'error': 'Error in edit_car()', 'details': str(e)}), 500
  finally:
    db.session.close()
    
def get_unsold_cars():
  with app.app_context():
    customer_car_view = db.Table('customer_car_view', db.MetaData(), autoload_with=db.engine)
  cars = db.session.query(customer_car_view).order_by(customer_car_view.c.timeCreated.asc()).all()
  cars_list = []
  for car in cars:
    cars_list.append(format_car(car))
  return {'cars': cars_list}

def batch_create_cars():
  car_data = request.json
  if not car_data:
    return jsonify({'error': 'car data not provided'}), 400
  cars = []
  for car_info in car_data:
    vin = car_info.get('vin')
    make = car_info.get('make')
    model = car_info.get('model')
    year = car_info.get('year')
    imageUrl = car_info.get('imageUrl')
    price = car_info.get('price')
    miles = car_info.get('miles')
    description = car_info.get('description')
    car_id = car_info.get('car_id')
    is_sold = car_info.get('is_sold')
      
    car = Car(vin, make, model, year, imageUrl, price, miles, description, car_id, is_sold)
    cars.append(car)
    db.session.add(car)
  try:
    db.session.commit()
    return 'cars added successfully'
  except Exception as e:
    db.session.rollback()
    return jsonify({'error': 'Failed to create batch cars', 'details': str(e)}), 500
  finally:
    db.session.close()
