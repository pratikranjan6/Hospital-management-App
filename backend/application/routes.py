from flask import current_app as app,jsonify,request ,abort
from .models import *
from .cache import cache_response, redis_client
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


@app.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.get_json(force=True, silent=False)
        if not data:
            return jsonify({"msg": "Invalid request format"}), 400
        
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({"msg": "Username and password are required"}), 400
        

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            access_token = create_access_token(identity=str(user.id))
            role = "admin" if getattr(user, 'admin', False) else "user"
            return jsonify(access_token=access_token, role=role), 200


        doctor = Doctor.query.filter_by(username=username).first()
        if doctor and doctor.password == password:
            access_token = create_access_token(identity=str(doctor.id))
            return jsonify(access_token=access_token, role='doctor'), 200

        return jsonify({"msg": "Wrong username or password"}), 400
    except Exception as e:
        app.logger.exception('Error in login')
        return jsonify({"msg": "Login failed: " + str(e)}), 500

@app.route('/api/login', methods=['GET'])
@jwt_required()
def login_get():
    try:
        identity = get_jwt_identity()
        try:
            user_id = int(identity)
        except Exception:
            return jsonify({'msg': 'Invalid user identity'}), 400
        

        user = User.query.get(user_id)
        if user:
            role = "admin" if getattr(user, 'admin', False) else "user"
            user_data = {
                'id': user.id,
                'username': user.username,
                'full_name': getattr(user, 'full_name', None),
                'address': getattr(user, 'address', None)
            }
            return jsonify({'user': user_data, 'role': role}), 200
        

        doctor = Doctor.query.get(user_id)
        if doctor:
            user_data = {
                'id': doctor.id,
                'username': doctor.username,
                'name': doctor.name,
                'specialization': doctor.department.name if doctor.department else 'N/A'
            }
            return jsonify({'user': user_data, 'role': 'doctor'}), 200
        
        return jsonify({'msg': 'User not found'}), 404
    except Exception as e:
        app.logger.exception('Error in login_get')
        return jsonify({'msg': 'Failed to retrieve user'}), 500



@app.route('/api/patient/profile', methods=['GET'])
@jwt_required()
def get_patient_profile():
    """Get current user's patient profile"""
    try:
        identity = get_jwt_identity()
        try:
            user_id = int(identity)
        except Exception:
            return jsonify({'msg': 'Invalid user identity'}), 400
        
        patient = Patient.query.filter_by(user_id=user_id).first()
        
        if not patient:
            return jsonify({
                'id': None,
                'user_id': user_id,
                'name': '',
                'age': None,
                'date_of_birth': None,
                'gender': '',
                'blood_group': '',
                'address': '',
                'exists': False
            }), 200
        
        return jsonify({
            'id': patient.id,
            'user_id': patient.user_id,
            'name': patient.name,
            'age': patient.age,
            'date_of_birth': patient.date_of_birth.isoformat() if patient.date_of_birth else None,
            'gender': patient.gender,
            'blood_group': patient.blood_group,
            'address': patient.address,
            'exists': True
        }), 200
    except Exception as e:
        app.logger.exception('Error fetching patient profile')
        return jsonify({'msg': 'Failed to fetch patient profile'}), 500


@app.route('/api/patient/profile', methods=['POST', 'PUT'])
@jwt_required()
def save_patient_profile():
    """Create or update patient profile for current user"""
    try:
        identity = get_jwt_identity()
        try:
            user_id = int(identity)
        except Exception:
            return jsonify({'msg': 'Invalid user identity'}), 400
        
        data = request.get_json()
        

        if not data.get('name') or not data.get('age') or not data.get('date_of_birth') or \
           not data.get('gender') or not data.get('blood_group'):
            return jsonify({'msg': 'Missing required fields'}), 400
        
        patient = Patient.query.filter_by(user_id=user_id).first()
        

        try:
            age = int(data.get('age'))
            if age < 0 or age > 150:
                return jsonify({'msg': 'Age must be between 0 and 150'}), 400
        except ValueError:
            return jsonify({'msg': 'Age must be a valid number'}), 400
        

        try:
            dob = datetime.strptime(data.get('date_of_birth'), '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'msg': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        if patient:

            patient.name = data.get('name')
            patient.age = age
            patient.date_of_birth = dob
            patient.gender = data.get('gender')
            patient.blood_group = data.get('blood_group')
            if data.get('address'):
                patient.address = data.get('address')
            
            db.session.commit()
            return jsonify({
                'msg': 'Patient profile updated successfully',
                'id': patient.id,
                'date_of_birth': patient.date_of_birth.isoformat()
            }), 200
        else:

            user = User.query.get(user_id)
            if not user:
                return jsonify({'msg': 'User not found'}), 404
            
            address = data.get('address') or user.address or 'Not Specified'
            
            new_patient = Patient(
                user_id=user_id,
                name=data.get('name'),
                age=age,
                date_of_birth=dob,
                gender=data.get('gender'),
                blood_group=data.get('blood_group'),
                address=address
            )
            
            db.session.add(new_patient)
            db.session.commit()
            
            return jsonify({
                'msg': 'Patient profile created successfully',
                'id': new_patient.id,
                'date_of_birth': new_patient.date_of_birth.isoformat()
            }), 201
    except Exception as e:
        db.session.rollback()
        app.logger.exception('Error saving patient profile')
        return jsonify({'msg': 'Failed to save patient profile'}), 500




@app.route('/api/patient/export_history', methods=['POST'])
@jwt_required()
def trigger_export_history():
    identity = get_jwt_identity()
    if not identity:
        return jsonify({'msg': 'Missing authentication token'}), 401
    try:
        user_id = int(identity)
    except Exception:
        return jsonify({'msg': 'Invalid identity'}), 400

    from .tasks import export_patient_history
    export_patient_history.delay(user_id)
    from .cache import redis_client
    redis_client.delete(f"export_done:{user_id}")
    return jsonify({'msg': 'Export job started; you will receive an email shortly'}), 202


@app.route('/api/patient/export_status', methods=['GET'])
@jwt_required()
def export_status():
    identity = get_jwt_identity()
    if not identity:
        return jsonify({'msg': 'Missing authentication token'}), 401
    try:
        user_id = int(identity)
    except Exception:
        return jsonify({'msg': 'Invalid identity'}), 400
    from .cache import redis_client
    done = redis_client.get(f"export_done:{user_id}")
    return jsonify({'done': bool(done)}), 200


@app.route('/api/admin/doctors', methods=['GET'])
@jwt_required()
@cache_response(expire=300)
def get_all_doctors():
    try:
        doctors = Doctor.query.all()
        doctors_data = []
        for doctor in doctors:
            doctors_data.append({
                'id': doctor.id,
                'username': doctor.username,
                'password': doctor.password,
                'name': doctor.name,
                'specialization': doctor.department.name if doctor.department else 'N/A',
                'qualification': doctor.qualification,
                'experience': doctor.experience,
                'availability': [
                    {
                        'id': a.id,
                        'date': a.date.isoformat() if getattr(a, 'date', None) else None,
                        'status': a.status
                    } for a in (doctor.availability or [])
                ]
            })
        return jsonify(doctors_data), 200
    except Exception as e:
        app.logger.exception('Error retrieving doctors')
        return jsonify({'msg': 'Failed to retrieve doctors'}), 500


@app.route('/api/admin/patients', methods=['GET'])
@jwt_required()
@cache_response(expire=300)
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
        app.logger.exception('Error retrieving appointments')
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
        app.logger.exception('Search error')
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
        try:
            redis_client.delete('cache:/api/admin/doctors?')
        except Exception:
            pass
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
        try:
            redis_client.delete('cache:/api/admin/doctors?')
        except Exception:
            pass
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
        try:
            redis_client.delete('cache:/api/admin/patients?')
        except Exception:
            pass
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
        try:
            redis_client.delete('cache:/api/admin/patients?')
        except Exception:
            pass
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
        if not data.get('username') or not data.get('password') or not data.get('name') or data.get('specialization') is None or not data.get('qualification'):
            return jsonify({'msg': 'Missing required fields'}), 400

        try:
            spec_id = int(data.get('specialization'))
        except Exception:
            return jsonify({'msg': 'Invalid specialization id'}), 400

        dept = Department.query.get(spec_id)
        if not dept:
            return jsonify({'msg': 'Specialization/Department not found'}), 400

        existing_doc = Doctor.query.filter_by(username=data.get('username')).first()
        existing_user = User.query.filter_by(username=data.get('username')).first()
        if existing_doc or existing_user:
            return jsonify({'msg': 'Username already exists'}), 400

        new_doctor = Doctor(
            username=data.get('username'),
            password=data.get('password'),
            name=data.get('name'),
            specialization=spec_id,
            qualification=data.get('qualification'),
            experience=data.get('experience', 0)
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


@app.route('/api/doctor/appointments', methods=['GET'])
@jwt_required()
def doctor_appointments():
    try:
        username = request.args.get('username')
        if username:
            doctor = Doctor.query.filter_by(username=username).first()
            if not doctor:
                return jsonify([]), 200
        else:
            identity = get_jwt_identity()
            try:
                doctor_id = int(identity)
            except Exception:
                return jsonify([]), 200
            doctor = Doctor.query.get(doctor_id)
            if not doctor:
                return jsonify([]), 200

        appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
        data = []
        for a in appointments:
            data.append({
                'id': a.id,
                'patient_id': a.patient.id if a.patient else None,
                'patient_name': a.patient.name if a.patient else 'N/A',
                'appointment_date': a.appointment_date.isoformat() if a.appointment_date else None,
                'status': a.status
            })
        return jsonify(data), 200
    except Exception as e:
        app.logger.exception('Error fetching doctor appointments')
        return jsonify({'msg': 'Failed to retrieve appointments'}), 500


@app.route('/api/doctor/patients', methods=['GET'])
@jwt_required()
def doctor_patients():
    try:
        username = request.args.get('username')
        if username:
            doctor = Doctor.query.filter_by(username=username).first()
            if not doctor:
                return jsonify([]), 200
        else:
            identity = get_jwt_identity()
            try:
                doctor_id = int(identity)
            except Exception:
                return jsonify([]), 200
            doctor = Doctor.query.get(doctor_id)
            if not doctor:
                return jsonify([]), 200

        appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
        patients_map = {}
        for a in appointments:
            if a.patient:
                p = a.patient
                patients_map[p.id] = {
                    'id': p.id,
                    'name': p.name,
                    'age': p.age,
                    'gender': p.gender,
                    'blood_group': p.blood_group
                }

        return jsonify(list(patients_map.values())), 200
    except Exception as e:
        app.logger.exception('Error fetching doctor patients')
        return jsonify({'msg': 'Failed to retrieve patients'}), 500





@app.route('/api/appointment/<int:appointment_id>', methods=['GET'])
@jwt_required()
def get_appointment(appointment_id):
    try:
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return jsonify({'msg': 'Appointment not found'}), 404
        
        return jsonify({
            'id': appointment.id,
            'patient_id': appointment.patient_id,
            'patient_name': appointment.patient.name if appointment.patient else None,
            'doctor_id': appointment.doctor_id,
            'doctor_name': appointment.doctor.name if appointment.doctor else None,
            'department_id': appointment.department_id,
            'department_name': appointment.department.name if appointment.department else None,
            'appointment_date': appointment.appointment_date.isoformat() if appointment.appointment_date else None,
            'status': appointment.status,
            'tests_done': appointment.tests_done or '',
            'diagnosis': appointment.diagnosis or '',
            'prescription': appointment.prescription or '',
            'medicines': appointment.medicines or ''
        }), 200
    except Exception as e:
        app.logger.exception('Error fetching appointment')
        return jsonify({'msg': 'Failed to fetch appointment'}), 500


@app.route('/api/appointment/<int:appointment_id>/history', methods=['PUT'])
@jwt_required()
def update_appointment_history(appointment_id):
    try:
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return jsonify({'msg': 'Appointment not found'}), 404
        
  
        identity = get_jwt_identity()
        try:
            doctor_id = int(identity)
        except Exception:
            doctor_id = None
        if doctor_id and appointment.doctor_id != doctor_id:
            return jsonify({'msg': 'Not authorized'}), 403
        
        data = request.get_json() or {}
        appointment.tests_done = data.get('tests_done', appointment.tests_done)
        appointment.diagnosis = data.get('diagnosis', appointment.diagnosis)
        appointment.prescription = data.get('prescription', appointment.prescription)
        appointment.medicines = data.get('medicines', appointment.medicines)

        try:
            ph = patient_history.query.filter_by(appointment_id=appointment.id).first()
            if ph:
                ph.diagnosis = appointment.diagnosis or ph.diagnosis
                ph.test_done = appointment.tests_done or ph.test_done
                ph.prescription = appointment.prescription or ph.prescription
                ph.medication = appointment.medicines or ph.medication
                ph.appointment_date = appointment.appointment_date or ph.appointment_date
            else:
                ph = patient_history(
                    patient_id=appointment.patient_id or 0,
                    doctor_id=appointment.doctor_id,
                    department_id=appointment.department_id,
                    appointment_id=appointment.id,
                    appointment_date=appointment.appointment_date,
                    diagnosis=appointment.diagnosis or '',
                    test_done=appointment.tests_done or '',
                    prescription=appointment.prescription or '',
                    medication=appointment.medicines or ''
                )
                db.session.add(ph)
        except Exception:
            app.logger.exception('patient_history upsert failed')

        db.session.commit()
        return jsonify({'msg': 'History updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        app.logger.exception('Error updating appointment history')
        return jsonify({'msg': 'Failed to update history'}), 500



@app.route('/api/doctor/<int:doctor_id>/availability', methods=['GET'])
@jwt_required()
def get_doctor_availability(doctor_id):
    try:
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return jsonify({'msg': 'Doctor not found'}), 404
        avails = Availability.query.filter_by(doctor_id=doctor_id).order_by(Availability.date).all()
        data = []
        for a in avails:
            data.append({
                'id': a.id,
                'doctor_id': a.doctor_id,
                'date': a.date.isoformat() if a.date else None,
                'status': a.status
            })
        return jsonify(data), 200
    except Exception as e:
        app.logger.exception('Error fetching doctor availability')
        return jsonify({'msg': 'Failed to fetch availability'}), 500


@app.route('/api/doctor/availability/<int:availability_id>', methods=['PUT'])
@jwt_required()
def toggle_availability_status(availability_id):
    try:
        avail = Availability.query.get(availability_id)
        if not avail:
            return jsonify({'msg': 'Availability not found'}), 404
        if avail.status and avail.status.lower() == 'available':
            avail.status = 'Not Available'
        else:
            avail.status = 'Available'
        db.session.commit()
        return jsonify({'id': avail.id, 'status': avail.status}), 200
    except Exception as e:
        db.session.rollback()
        app.logger.exception('Error updating availability')
        return jsonify({'msg': 'Failed to update availability'}), 500




@app.route('/api/patient/<int:patient_id>/history', methods=['GET'])
@jwt_required()
def get_patient_history(patient_id):
    try:
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({'msg': 'Patient not found'}), 404
        records = patient_history.query.filter_by(patient_id=patient_id).order_by(patient_history.appointment_date.desc()).all()

        history = []
        for r in records:
            meds = r.medication.split(',') if r.medication else []
            history.append({
                'id': r.id,
                'appointment_id': r.appointment_id,
                'appointment_date': r.appointment_date.isoformat() if r.appointment_date else None,
                'diagnosis': r.diagnosis or '',
                'tests_done': r.test_done or '',
                'prescription': r.prescription or '',
                'medicines': meds,
                'doctor_name': r.doctor.name if getattr(r, 'doctor', None) else (Doctor.query.get(r.doctor_id).name if r.doctor_id else 'N/A'),
                'department': r.department.name if getattr(r, 'department', None) else (Department.query.get(r.department_id).name if r.department_id else 'N/A')
            })

        return jsonify({
            'patient_name': patient.name,
            'appointments': history
        }), 200
    except Exception as e:
        app.logger.exception('Error fetching patient history')
        return jsonify({'msg': 'Failed to fetch patient history'}), 500


@app.route('/api/departments', methods=['GET'])
@jwt_required()
@cache_response(expire=300)
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
        
        existing_dept = Department.query.filter_by(name=data.get('name')).first()
        if existing_dept:
            return jsonify({'msg': 'Department already exists'}), 400
        
        new_department = Department(
            name=data.get('name'),
            description=data.get('description')
        )
        
        db.session.add(new_department)
        db.session.commit()
        try:
            redis_client.delete('cache:/api/departments?')
        except Exception:
            pass
        
        return jsonify({
            'msg': 'Department created successfully',
            'department_id': new_department.id
        }), 201
    except Exception as e:
        db.session.rollback()
        app.logger.exception('Error creating department')
        return jsonify({'msg': 'Failed to create department'}), 500


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
        try:
            redis_client.delete('cache:/api/departments?')
        except Exception:
            pass
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

        linked_doctor = Doctor.query.filter_by(specialization=department_id).first()
        if linked_doctor:
            return jsonify({'msg': 'Cannot delete department with assigned doctors'}), 400

        db.session.delete(dept)
        db.session.commit()
        try:
            redis_client.delete('cache:/api/departments?')
        except Exception:
            pass
        return jsonify({'msg': 'Department deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        app.logger.exception('Error deleting department')
        return jsonify({'msg': 'Failed to delete department'}), 500



@app.route('/api/user/appointments', methods=['GET'])
@jwt_required()
def get_user_appointments():
    try:
        identity = get_jwt_identity()
        try:
            user_id = int(identity)
        except Exception:
            return jsonify({'msg': 'Invalid user identity'}), 400
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'msg': 'User not found'}), 404
        
        patients = Patient.query.filter_by(user_id=user_id).all()
        patient_ids = [p.id for p in patients]
        
        if not patient_ids:
            return jsonify([]), 200
            
        appointments = Appointment.query.filter(Appointment.patient_id.in_(patient_ids)).all()
        
        appointments_data = []
        for appointment in appointments:
            appointments_data.append({
                'id': appointment.id,
                'patient_id': appointment.patient_id,
                'patient_name': appointment.patient.name if appointment.patient else 'N/A',
                'doctor_id': appointment.doctor_id,
                'doctor_name': appointment.doctor.name if appointment.doctor else 'N/A',
                'department_id': appointment.department_id,
                'department_name': appointment.department.name if appointment.department else 'N/A',
                'appointment_date': appointment.appointment_date.isoformat() if appointment.appointment_date else '',
                'status': appointment.status,
                'tests_done': appointment.tests_done or '',
                'diagnosis': appointment.diagnosis or '',
                'prescription': appointment.prescription or '',
                'medicines': appointment.medicines or ''
            })
        
        return jsonify(appointments_data), 200
    except Exception as e:
        app.logger.exception('Error fetching user appointments')
        return jsonify({'msg': 'Failed to fetch appointments'}), 500


@app.route('/api/user/appointment/<int:appointment_id>', methods=['DELETE'])
@jwt_required()
def cancel_user_appointment(appointment_id):
    try:
        identity = get_jwt_identity()
        try:
            user_id = int(identity)
        except Exception:
            return jsonify({'msg': 'Invalid user identity'}), 400
        
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return jsonify({'msg': 'Appointment not found'}), 404
        
        if appointment.patient and appointment.patient.user_id != user_id:
            return jsonify({'msg': 'Not authorized'}), 403
        
        appointment.status = 'Open'
        db.session.commit()
        
        return jsonify({'msg': 'Appointment cancelled (slot reopened) successfully'}), 200
    except Exception as e:
        db.session.rollback()
        app.logger.exception('Error cancelling appointment')
        return jsonify({'msg': 'Failed to cancel appointment'}), 500


@app.route('/api/department/<int:department_id>/doctors', methods=['GET'])
@jwt_required()
def get_department_doctors(department_id):
    try:
        department = Department.query.get(department_id)
        if not department:
            return jsonify({'msg': 'Department not found'}), 404
        
        doctors = Doctor.query.filter_by(specialization=department_id).all()
        
        doctors_data = []
        for doctor in doctors:
            doctors_data.append({
                'id': doctor.id,
                'name': doctor.name,
                'specialization': doctor.department.name if doctor.department else 'N/A',
                'specialization_id': doctor.specialization,
                'qualification': doctor.qualification,
                'experience': doctor.experience,
                'username': doctor.username
            })
        
        return jsonify(doctors_data), 200
    except Exception as e:
        app.logger.exception('Error fetching department doctors')
        return jsonify({'msg': 'Failed to fetch doctors'}), 500


@app.route('/api/doctors/<int:doctor_id>', methods=['GET'])
@jwt_required()
def get_doctor_by_id(doctor_id):
    try:
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return jsonify([]), 200
        
        return jsonify([{
            'id': doctor.id,
            'name': doctor.name,
            'specialization': doctor.department.name if doctor.department else 'N/A',
            'specialization_id': doctor.specialization,
            'qualification': doctor.qualification,
            'experience': doctor.experience,
            'username': doctor.username
        }]), 200
    except Exception as e:
        app.logger.exception('Error fetching doctor')
        return jsonify([]), 200


@app.route('/api/doctor/<int:doctor_id>/7day-slots', methods=['GET'])
@jwt_required()
def get_7day_slots(doctor_id):
    try:
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return jsonify({'msg': 'Doctor not found'}), 404
        
        slots = []
        today = datetime.now().date()
        
        for i in range(7):
            current_date = today + timedelta(days=i)
            day_of_week = current_date.strftime('%a')  
            date_number = current_date.day
            month = current_date.strftime('%b') 
            

            day_num = current_date.weekday()  
            is_available = day_num < 5  
      
            availability = Availability.query.filter_by(
                doctor_id=doctor_id,
                date=current_date
            ).first()
            
            if availability:
                is_available = availability.status.lower() == 'available'
            
         
            appointments_on_date = Appointment.query.filter(
                Appointment.doctor_id == doctor_id,
                Appointment.appointment_date >= datetime.combine(current_date, datetime.min.time()),
                Appointment.appointment_date < datetime.combine(current_date + timedelta(days=1), datetime.min.time()),
                Appointment.status == 'Booked'
            ).all()
            
            is_fully_booked = len(appointments_on_date) > 0
            
            slot_status = 'Booked' if is_fully_booked else 'Open'
            
            slots.append({
                'id': f'slot-{doctor_id}-{current_date.isoformat()}',
                'doctorId': doctor_id,
                'date': current_date.isoformat(),
                'dateNumber': date_number,
                'month': month,
                'dayOfWeek': day_of_week,
                'startTime': '09:00',
                'endTime': '17:00',
                'available': is_available,
                'status': slot_status,
                'bookedByMe': False,
                'appointmentId': appointments_on_date[0].id if is_fully_booked else None
            })
        
        return jsonify(slots), 200
    except Exception as e:
        app.logger.exception('Error fetching 7-day slots')
        return jsonify({'msg': 'Failed to fetch slots'}), 500


@app.route('/api/appointment/book', methods=['POST'])
@jwt_required()
def book_appointment():
    try:
        data = request.get_json()
        
        if not data.get('patient_id') or not data.get('doctor_id') or not data.get('appointment_date'):
            return jsonify({'msg': 'Missing required fields'}), 400
        
        patient = Patient.query.get(data.get('patient_id'))
        if not patient:
            return jsonify({'msg': 'Patient not found'}), 404
        
        doctor = Doctor.query.get(data.get('doctor_id'))
        if not doctor:
            return jsonify({'msg': 'Doctor not found'}), 404
        
        department_id = doctor.specialization if doctor.specialization else data.get('department_id', 1)
        
        try:
            appointment_date = datetime.fromisoformat(data.get('appointment_date').replace('Z', '+00:00'))
        except Exception:
            return jsonify({'msg': 'Invalid appointment date format'}), 400
        
     
        existing = Appointment.query.filter(
            Appointment.patient_id == data.get('patient_id'),
            Appointment.doctor_id == data.get('doctor_id'),
            Appointment.appointment_date >= appointment_date.replace(hour=0, minute=0, second=0),
            Appointment.appointment_date < appointment_date.replace(hour=23, minute=59, second=59),
            Appointment.status == 'Booked'
        ).first()
        
        if existing:
            return jsonify({'msg': 'You already have an appointment with this doctor on this date'}), 400
        
     
        new_appointment = Appointment(
            patient_id=data.get('patient_id'),
            doctor_id=data.get('doctor_id'),
            department_id=department_id,
            appointment_date=appointment_date,
            status='Booked'
        )
        
        db.session.add(new_appointment)
        db.session.commit()
        
        return jsonify({
            'msg': 'Appointment booked successfully',
            'appointment_id': new_appointment.id,
            'appointment_date': new_appointment.appointment_date.isoformat()
        }), 201
    except Exception as e:
        db.session.rollback()
        app.logger.exception('Error booking appointment')
        return jsonify({'msg': 'Failed to book appointment'}), 500


@app.route('/api/doctor/appointment/<int:appointment_id>/cancel', methods=['POST'])
@jwt_required()
def doctor_cancel_appointment(appointment_id):
    try:
        identity = get_jwt_identity()
        try:
            doctor_id = int(identity)
        except Exception:
            return jsonify({'msg': 'Invalid doctor identity'}), 400
        
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return jsonify({'msg': 'Appointment not found'}), 404
        
        if appointment.doctor_id != doctor_id:
            return jsonify({'msg': 'Not authorized'}), 403
        
        appointment.status = 'Open'
        db.session.commit()
        return jsonify({'msg': 'Appointment cancelled (slot reopened) successfully'}), 200
    except Exception as e:
        db.session.rollback()
        app.logger.exception('Error doctor cancelling appointment')
        return jsonify({'msg': 'Failed to cancel appointment'}), 500


@app.route('/api/doctor/appointment/<int:appointment_id>/complete', methods=['POST'])
@jwt_required()
def doctor_complete_appointment(appointment_id):
    try:
        identity = get_jwt_identity()
        try:
            doctor_id = int(identity)
        except Exception:
            return jsonify({'msg': 'Invalid doctor identity'}), 400
        
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return jsonify({'msg': 'Appointment not found'}), 404
        
        if appointment.doctor_id != doctor_id:
            return jsonify({'msg': 'Not authorized'}), 403
        
        appointment.status = 'Open'
        db.session.commit()
        return jsonify({'msg': 'Appointment marked complete (slot reopened)'}), 200
    except Exception as e:
        db.session.rollback()
        app.logger.exception('Error doctor completing appointment')
        return jsonify({'msg': 'Failed to complete appointment'}), 500