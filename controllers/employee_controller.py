# from flask import jsonify, request
# from models.employee import Employee
# from app import db


# def format_employee(employee): 
#   return {
#     "id": employee.id,
#     "username": employee.username,
#     "name" : employee.name,
#     "emp_role": employee.emp_role,
#     "imageUrl": employee.imageUrl,
#     "xUrl": employee.xUrl,
#     "linkedinUrl": employee.linkedinUrl
#   }
  
# def create_employee():
#   data = request.json
#   if ('name') not in data:
#     return jsonify({'error': 'name not provided'}), 400
  
#   if ('username') not in data:
#     return jsonify({'error': 'username not provided'}), 400
  
#   if ('password') not in data:
#     return jsonify({'error': 'password not provided'}), 400
  
#   name = data.get('name')
#   username = data.get('username')
#   password = data.get('password')
#   emp_role = data.get('emp_role')
#   imageUrl = data.get('imageUrl')
#   xUrl = data.get('xUrl')
#   linkedinUrl = data.get('linkedinUrl')
  
#   employee = Employee(name, username, password, emp_role, imageUrl, xUrl, linkedinUrl)
#   db.session.add(employee)
  
#   try:
#     db.session.commit()
#     return format_employee(employee)
#   except Exception as e:
#     db.session.rollback()
#     return jsonify({'error': 'Error in create_employee()', 'details': str(e)}), 500
#   finally:
#     db.session.close()

# def delete_employee(id):
#   employee = db.session.get(Employee, id)
#   if not employee:
#     return jsonify({"error": "Employee not found"}), 404
#   try:
#     db.session.delete(employee)
#     db.session.commit()
#     return f'Employee (id: {id}) deleted!'
#   except Exception as e:
#     return jsonify({'error': 'Error in delete_employee()', 'details': str(e)}), 500
#   finally:
#     db.session.close()
    
# def update_employee(id):
#   employee = db.session.get(Employee, id)
#   if not employee:
#       return jsonify({"error": "Employee not found"}), 404
  
#   data = request.json
#   employee.name = data.get('name', employee.name)
#   employee.emp_role = data.get('emp_role', employee.emp_role)
#   employee.imageUrl = data.get('imageUrl', employee.imageUrl)
#   employee.xUrl = data.get('xUrl', employee.xUrl)
#   employee.linkedinUrl = data.get('linkedinUrl', employee.linkedinUrl)
#   employee.timeCreated = data.get('timeCreated', employee.timeCreated)
#   employee.username = data.get('username', employee.username)

#   try:
#     db.session.commit()
#     return {'employee': format_employee(employee)}
#   except Exception as e:
#     return jsonify({'error': 'Error in edit_employee()', 'details': str(e)}), 500
#   finally:
#     db.session.close()
    
# def get_employee(id):
#   employee = db.session.get(Employee, id)
#   if not employee:
#     return jsonify({"error": "Employee not found"}), 404
#   return {'employee': format_employee(employee)}

# def get_employees():
#   employees = Employee.query.order_by(Employee.timeCreated).all()
#   employees_list = []
#   for employee in employees:
#     employees_list.append(format_employee(employee))
#   return {'employees': employees_list}

# def batch_create_employees():
#   employee_data = request.json
#   if not employee_data:
#     return jsonify({'error': 'employee data not provided'}), 400
#   employees = []
#   for employee_info in employee_data:
#     name = employee_info.get('name')
#     username = employee_info.get('username')
#     password = employee_info.get('password')
#     emp_role = employee_info.get('emp_role')
#     imageUrl = employee_info.get('imageUrl')
#     xUrl = employee_info.get('xUrl')
#     linkedinUrl = employee_info.get('linkedinUrl')
    
#     employee = Employee(name, username, password, emp_role, imageUrl, xUrl, linkedinUrl)
#     employees.append(employee)
#   try:
#     db.session.add_all(employees)
#     db.session.commit()
#     return 'employees added successfully'
#   except Exception as e:
#     db.session.rollback()
#     return jsonify({'error': 'Failed to create batch employees', 'details': str(e)}), 500
#   finally:
#     db.session.close()
  