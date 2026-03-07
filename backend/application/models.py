from .database import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, default=False)
    
    patients = db.relationship('Patient', backref='user', lazy=True, cascade='all, delete-orphan')

class Doctor(db.Model):
    __tablename__ = "doctor"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    specialization = db.Column(db.Integer, db.ForeignKey("department.id"), nullable=False)   
    qualification = db.Column(db.String, nullable=False)
    experience = db.Column(db.Integer, nullable=False)    

    department = db.relationship('Department', backref='doctors', lazy=True)
    appointments = db.relationship('Appointment', backref='doctor', lazy=True, cascade='all, delete-orphan')
    availability = db.relationship('Availability', backref='doctor', lazy=True, cascade='all, delete-orphan')
    patient_history = db.relationship('patient_history', backref='doctor', lazy=True, cascade='all, delete-orphan')


class Patient(db.Model):
    __tablename__ = "patient"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String, nullable=False)
    blood_group = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    
    appointments = db.relationship('Appointment', backref='patient', lazy=True, cascade='all, delete-orphan')
    patient_history = db.relationship('patient_history', backref='patient', lazy=True, cascade='all, delete-orphan')


class Department(db.Model):
    __tablename__ = "department"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    

    appointments = db.relationship('Appointment', backref='department', lazy=True, cascade='all, delete-orphan')
    patient_history = db.relationship('patient_history', backref='department', lazy=True, cascade='all, delete-orphan')

class Appointment(db.Model):
    __tablename__ = "appointment"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String, nullable=False, default='Open')
    tests_done = db.Column(db.String, nullable=True, default='')
    diagnosis = db.Column(db.String, nullable=True, default='')
    prescription = db.Column(db.String, nullable=True, default='')
    medicines = db.Column(db.String, nullable=True, default='')

    patient_history = db.relationship('patient_history', backref='appointment', lazy=True, cascade='all, delete-orphan')


class Availability(db.Model):
    __tablename__ = "availability"
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String, nullable=False, default='Not Available') 

class patient_history(db.Model):
    __tablename__ = "patient_history"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointment.id"), nullable=False) 
    appointment_date = db.Column(db.DateTime, nullable=False)
    diagnosis = db.Column(db.String, nullable=True)
    test_done = db.Column(db.String, nullable=True)
    prescription = db.Column(db.String, nullable=True)
    medication = db.Column(db.String, nullable=True)