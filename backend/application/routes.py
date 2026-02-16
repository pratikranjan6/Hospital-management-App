from flask import current_app as app,jsonify,request ,abort
from .models import *
from flask_jwt_extended import create_access_token,current_user, jwt_required,get_jwt_identity
from functools import wraps
from datetime import datetime,timedelta


def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            if current_user.role != required_role:
                return jsonify(message = "you are not authorized"),403
            return fn(*args, **kwargs)
        return decorator
    return wrapper


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    full_name = data.get("full_name")
    address = data.get("address")

    if not username or not full_name or not password or not address:
        return jsonify({"msg": "Missing required fields"}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"msg": "Username already exists"}), 400

    new_user = User(
        username=username,
        password=password,
        full_name=full_name,
        address=address
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or user.password != password:
        return jsonify({"msg": "Wrong username or password"}), 400

    access_token = create_access_token(identity=str(user.id))
    role = "admin" if getattr(user, 'admin', False) else "user"
    return jsonify(access_token=access_token, role=role), 200

@app.route('/api/login', methods=['GET'])
@jwt_required()
def login_get():
    try:
        user = current_user
        role = "admin" if getattr(user, 'admin', False) else "user"
        user_data = {
            'id': user.id,
            'username': user.username,
            'full_name': getattr(user, 'full_name', None),
            'address': getattr(user, 'address', None),
            'pin_code': getattr(user, 'pin_code', None)
        }
        return jsonify({'user': user_data, 'role': role}), 200
    except Exception as e:
        app.logger.exception('Error in login_get')
        return jsonify({'msg': 'Failed to retrieve user'}), 500

# Admin Dashboard Routes

@app.route('/api/admin/doctors', methods=['GET'])
@jwt_required()
def get_all_doctors():
    try:
        doctors = Doctor.query.all()
        doctors_data = []
        for doctor in doctors:
            doctors_data.append({
                'id': doctor.id,
                'name': doctor.name,
                'specialization': doctor.department.name if doctor.department else 'N/A',
                'qualification': doctor.qualification,
                'experience': doctor.experience,
                'availability': doctor.availability
            })
        return jsonify(doctors_data), 200
    except Exception as e:
        return jsonify({'msg': 'Failed to retrieve doctors'}), 500


@app.route('/api/admin/patients', methods=['GET'])
@jwt_required()
def get_all_patients():
    try:
        patients = Patient.query.all()
        patients_data = []
        for patient in patients:
            patients_data.append({
                'id': patient.id,
                'name': patient.name,
                'age': patient.age,
                'gender': patient.gender,
                'blood_group': patient.blood_group,
                'address': patient.address,
                'date_of_birth': patient.date_of_birth.isoformat() if patient.date_of_birth else ''
            })
        return jsonify(patients_data), 200
    except Exception as e:
        return jsonify({'msg': 'Failed to retrieve patients'}), 500


@app.route('/api/admin/appointments', methods=['GET'])
@jwt_required()
def get_all_appointments():
    try:
        appointments = Appointment.query.all()
        appointments_data = []
        for appointment in appointments:
            appointments_data.append({
                'id': appointment.id,
                'patient_name': appointment.patient.name if appointment.patient else 'N/A',
                'doctor_name': appointment.doctor.name if appointment.doctor else 'N/A',
                'department': appointment.department.name if appointment.department else 'N/A',
                'appointment_date': appointment.appointment_date.isoformat() if appointment.appointment_date else '',
                'status': appointment.status
            })
        return jsonify(appointments_data), 200
    except Exception as e:
        return jsonify({'msg': 'Failed to retrieve appointments'}), 500


@app.route('/api/admin/search', methods=['GET'])
@jwt_required()
def search_entities():
    try:
        query = request.args.get('q', '').lower()
        if not query:
            return jsonify({'msg': 'Search query required'}), 400
        
        doctors = Doctor.query.filter(Doctor.name.ilike(f'%{query}%')).all()
        patients = Patient.query.filter(Patient.name.ilike(f'%{query}%')).all()
        
        results = {
            'doctors': [{
                'id': d.id,
                'name': d.name,
                'specialization': d.department.name if d.department else 'N/A'
            } for d in doctors],
            'patients': [{
                'id': p.id,
                'name': p.name,
                'age': p.age
            } for p in patients]
        }
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'msg': 'Search failed'}), 500


@app.route('/api/admin/doctor/<int:doctor_id>', methods=['PUT'])
@jwt_required()
def update_doctor(doctor_id):
    try:
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return jsonify({'msg': 'Doctor not found'}), 404
        
        data = request.get_json()
        if 'name' in data:
            doctor.name = data['name']
        if 'qualification' in data:
            doctor.qualification = data['qualification']
        if 'experience' in data:
            doctor.experience = data['experience']
        if 'availability' in data:
            doctor.availability = data['availability']
        
        db.session.commit()
        return jsonify({'msg': 'Doctor updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Failed to update doctor'}), 500


@app.route('/api/admin/doctor/<int:doctor_id>', methods=['DELETE'])
@jwt_required()
def delete_doctor(doctor_id):
    try:
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return jsonify({'msg': 'Doctor not found'}), 404
        
        db.session.delete(doctor)
        db.session.commit()
        return jsonify({'msg': 'Doctor deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Failed to delete doctor'}), 500


@app.route('/api/admin/doctor/<int:doctor_id>/blacklist', methods=['POST'])
@jwt_required()
def blacklist_doctor(doctor_id):
    try:
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return jsonify({'msg': 'Doctor not found'}), 404
        
        # Mark doctor as unavailable (blacklist)
        doctor.availability = 'blacklisted'
        db.session.commit()
        return jsonify({'msg': 'Doctor blacklisted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Failed to blacklist doctor'}), 500


@app.route('/api/admin/patient/<int:patient_id>', methods=['PUT'])
@jwt_required()
def update_patient(patient_id):
    try:
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({'msg': 'Patient not found'}), 404
        
        data = request.get_json()
        if 'name' in data:
            patient.name = data['name']
        if 'age' in data:
            patient.age = data['age']
        if 'gender' in data:
            patient.gender = data['gender']
        if 'blood_group' in data:
            patient.blood_group = data['blood_group']
        if 'address' in data:
            patient.address = data['address']
        
        db.session.commit()
        return jsonify({'msg': 'Patient updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Failed to update patient'}), 500


@app.route('/api/admin/patient/<int:patient_id>', methods=['DELETE'])
@jwt_required()
def delete_patient(patient_id):
    try:
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({'msg': 'Patient not found'}), 404
        
        db.session.delete(patient)
        db.session.commit()
        return jsonify({'msg': 'Patient deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Failed to delete patient'}), 500


@app.route('/api/admin/patient/<int:patient_id>/blacklist', methods=['POST'])
@jwt_required()
def blacklist_patient(patient_id):
    try:
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({'msg': 'Patient not found'}), 404
        
        # Add blacklist flag to patient (would need to add is_blacklisted field to model)
        # For now, marking address as 'BLACKLISTED'
        patient.address = 'BLACKLISTED'
        db.session.commit()
        return jsonify({'msg': 'Patient blacklisted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Failed to blacklist patient'}), 500


@app.route('/api/admin/doctor', methods=['POST'])
@jwt_required()
def create_doctor():
    try:
        data = request.get_json()
        
        if not data.get('name') or not data.get('specialization') or not data.get('qualification'):
            return jsonify({'msg': 'Missing required fields'}), 400
        
        # Get current user
        user_id = get_jwt_identity()
        
        new_doctor = Doctor(
            user_id=user_id,
            name=data.get('name'),
            specialization=data.get('specialization'),
            qualification=data.get('qualification'),
            experience=data.get('experience', 0),
            availability=data.get('availability', 'Available')
        )
        
        db.session.add(new_doctor)
        db.session.commit()
        
        return jsonify({
            'msg': 'Doctor created successfully',
            'doctor_id': new_doctor.id
        }), 201
    except Exception as e:
        db.session.rollback()
        app.logger.exception('Error creating doctor')
        return jsonify({'msg': 'Failed to create doctor'}), 500


@app.route('/api/patient/<int:patient_id>/history', methods=['GET'])
@jwt_required()
def get_patient_history(patient_id):
    try:
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({'msg': 'Patient not found'}), 404
        
        appointments = Appointment.query.filter_by(patient_id=patient_id).all()
        
        appointments_data = []
        for appointment in appointments:
            appointments_data.append({
                'id': appointment.id,
                'visit_type': appointment.status,
                'tests_done': 'ECG',  # Can be extended from appointment model
                'diagnosis': 'Abnormal',  # Can be extended from appointment model
                'prescription': 'Daily exercise',  # Can be extended from appointment model
                'medicines': ['Medicine 1', 'Medicine 2', 'Medicine 3']  # Can be extended from appointment model
            })
        
        return jsonify({
            'patient_name': patient.name,
            'doctor_name': appointments[0].doctor.name if appointments and appointments[0].doctor else 'N/A',
            'department': appointments[0].department.name if appointments and appointments[0].department else 'N/A',
            'appointments': appointments_data
        }), 200
    except Exception as e:
        app.logger.exception('Error fetching patient history')
        return jsonify({'msg': 'Failed to fetch patient history'}), 500


@app.route('/api/departments', methods=['GET'])
@jwt_required()
def get_departments():
    try:
        departments = Department.query.all()
        departments_data = []
        for dept in departments:
            departments_data.append({
                'id': dept.id,
                'name': dept.name,
                'description': dept.description
            })
        return jsonify(departments_data), 200
    except Exception as e:
        app.logger.exception('Error fetching departments')
        return jsonify({'msg': 'Failed to fetch departments'}), 500


@app.route('/api/admin/department', methods=['POST'])
@jwt_required()
def create_department():
    try:
        data = request.get_json()
        
        if not data.get('name') or not data.get('description'):
            return jsonify({'msg': 'Missing required fields'}), 400
        
        # Check if department already exists
        existing_dept = Department.query.filter_by(name=data.get('name')).first()
        if existing_dept:
            return jsonify({'msg': 'Department already exists'}), 400
        
        new_department = Department(
            name=data.get('name'),
            description=data.get('description')
        )
        
        db.session.add(new_department)
        db.session.commit()
        
        return jsonify({
            'msg': 'Department created successfully',
            'department_id': new_department.id
        }), 201
    except Exception as e:
        db.session.rollback()
        app.logger.exception('Error creating department')
        return jsonify({'msg': 'Failed to create department'}), 500


# CORS preflight (OPTIONS) for department update/delete - do not require auth
@app.route('/api/admin/department/<int:department_id>', methods=['OPTIONS'])
def department_options(department_id):
    return jsonify({}), 200


@app.route('/api/admin/department/<int:department_id>', methods=['PUT'])
@jwt_required()
def update_department(department_id):
    try:
        dept = Department.query.get(department_id)
        if not dept:
            return jsonify({'msg': 'Department not found'}), 404

        data = request.get_json() or {}
        if 'name' in data:
            existing = Department.query.filter(Department.name == data['name'], Department.id != department_id).first()
            if existing:
                return jsonify({'msg': 'Another department with this name exists'}), 400
            dept.name = data['name']
        if 'description' in data:
            dept.description = data['description']

        db.session.commit()
        return jsonify({'msg': 'Department updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        app.logger.exception('Error updating department')
        return jsonify({'msg': 'Failed to update department'}), 500


@app.route('/api/admin/department/<int:department_id>', methods=['DELETE'])
@jwt_required()
def delete_department(department_id):
    try:
        dept = Department.query.get(department_id)
        if not dept:
            return jsonify({'msg': 'Department not found'}), 404

        # Prevent deletion if doctors reference this department
        linked_doctor = Doctor.query.filter_by(specialization=department_id).first()
        if linked_doctor:
            return jsonify({'msg': 'Cannot delete department with assigned doctors'}), 400

        db.session.delete(dept)
        db.session.commit()
        return jsonify({'msg': 'Department deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        app.logger.exception('Error deleting department')
        return jsonify({'msg': 'Failed to delete department'}), 500