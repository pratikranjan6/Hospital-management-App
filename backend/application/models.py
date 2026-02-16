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
    
    doctors = db.relationship('Doctor', backref='user', lazy=True, cascade='all, delete-orphan')
    patients = db.relationship('Patient', backref='user', lazy=True, cascade='all, delete-orphan')

class Doctor(db.Model):
    __tablename__ = "doctor"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    specialization = db.Column(db.Integer, db.ForeignKey("department.id"), nullable=False)   
    qualification = db.Column(db.String, nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    availability = db.Column(db.String, nullable=False)
    

    department = db.relationship('Department', backref='doctors', lazy=True)
    appointments = db.relationship('Appointment', backref='doctor', lazy=True, cascade='all, delete-orphan')

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

class Department(db.Model):
    __tablename__ = "department"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    

    appointments = db.relationship('Appointment', backref='department', lazy=True, cascade='all, delete-orphan')


class Appointment(db.Model):
    __tablename__ = "appointment"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String, nullable=False)