# database.py - Database Operations
from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from models import db, Student
from datetime import datetime, timezone

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        print("✅ Database initialized successfully!")
        
        if Student.query.count() == 0:
            add_sample_data()

def add_sample_data():
    sample_students = [
        Student(
            student_name='John Doe',
            registration_number='STU2024001',
            email='john.doe@university.edu',
            programme='Computer Science'
        ),
        Student(
            student_name='Jane Smith',
            registration_number='STU2024002',
            email='jane.smith@university.edu',
            programme='Information Technology'
        )
    ]
    
    for student in sample_students:
        db.session.add(student)
    db.session.commit()
    print("📚 Sample data added!")

def get_all_students():
    return Student.query.filter_by(is_active=True).all()

def get_student_by_name(name):
    return Student.query.filter(
        Student.student_name.contains(name),
        Student.is_active == True
    ).all()

def get_student_by_registration(registration_number):
    return Student.query.filter_by(registration_number=registration_number).first()

def get_student_by_id(student_id):
    return Student.query.get(student_id)

def get_deleted_students():
    return Student.query.filter_by(is_active=False).all()

def add_student(student_data):
    try:
        existing = get_student_by_registration(student_data['registration_number'])
        if existing:
            return False, "Registration number already exists!", None
        
        existing_email = Student.query.filter_by(email=student_data['email']).first()
        if existing_email:
            return False, "Email already registered!", None
        
        new_student = Student(
            student_name=student_data['student_name'],
            registration_number=student_data['registration_number'],
            email=student_data['email'],
            programme=student_data['programme']
        )
        
        db.session.add(new_student)
        db.session.commit()
        return True, "Student registered successfully!", new_student
    
    except Exception as e:
        db.session.rollback()
        return False, f"Database error: {str(e)}", None
    
def update_student(student_id, update_data):
    student = get_student_by_id(student_id)
    
    if not student:
        return False, "Student not found"
    
    try:
        new_reg = update_data.get('registration_number')
        if new_reg and new_reg != student.registration_number:
            existing = get_student_by_registration(new_reg)
            if existing and existing.id != student.id:
                return False, "Registration number already exists"

        for key, value in update_data.items():
            if hasattr(student, key) and value is not None:
                setattr(student, key, value)
                    
        db.session.commit()
        return True, "Student updated successfully"
    except Exception as e:
        db.session.rollback()
        return False, f"Database error: {str(e)}"
    
def permanent_delete_student(student_id):
    student = get_student_by_registration(student_id)
    
    if not student:
        return False, "Student not found"
    try:
        db.session.delete(student)
        db.session.commit()
        return True, "Student deleted permanently"
    
    except Exception as e:
        print(f"ERROR: {e}")
        return False, f"Database error: {str(e)}"

def soft_delete_student(student_id):
    student = get_student_by_id(student_id)
    if not student:
        return False, "Student not found"
    try:
        student.is_active = False
        db.session.commit()
        return True, "Student deleted successfully"
    except Exception as e:
        db.session.rollback()
        return False, f"Database error: {str(e)}"

def restore_student(student_id):
    student = get_student_by_id(student_id)
    if not student:
        return False, "Student not found"
    try:
        student.is_active = True
        db.session.commit()
        return True, "Student restored successfully"
    
    except Exception as e:
        return False, f"Database error: {str(e)}"
    