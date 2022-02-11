import uuid

from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class Departament(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer(), primary_key=True)
    uuid = db.Column(db.String(36), unique=True)
    title = db.Column(db.String(120), nullable=False)
    employees = db.relationship('Employee', backref='departament', lazy='dynamic')
    average_salary = db.Column(db.Float(16))

    def __init__(self, title):
        self.title = title
        self.uuid = str(uuid.uuid4())
        self.average_salary = 0
        self.employees = []

    def add_employee(self, employee):
        self.employees.append(employee)
        employee.change_departament(self.uuid)
        self.update_avg_salary()

    def remove_employee(self, employee):
        self.employees.remove(employee)
        employee.change_departament()
        self.update_avg_salary()

    # Since self.employees is AppenderBaseQuery, it has no __len__() method, so len(self.employees) will throw error,
    # that's why .count() is used. Attention, it is Querry(some_entity).count() but not List.count(__value) method,
    # so IDE warning can be ignored.
    def update_avg_salary(self):
        self.average_salary = round(sum([employee.salary for employee in self.employees]) / self.employees.count(), 2)

    def __repr__(self):
        return f'Departament({self.title}, {self.average_salary})'


class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer(), primary_key=True)
    uuid = db.Column(db.String(36), unique=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    salary = db.Column(db.Float(16), nullable=False)
    departament_id = db.Column(db.String(36), db.ForeignKey('departments.uuid'))

    def __init__(self, first_name, last_name, salary, departament_uuid=None):
        self.first_name = first_name
        self.last_name = last_name
        self.salary = salary
        self.uuid = str(uuid.uuid4())
        self.departament_id = departament_uuid

    def change_departament(self, new_departament_uuid=None):
        self.departament_id = new_departament_uuid

    def __repr__(self):
        return f'Employee({self.first_name},{self.last_name}, {self.salary}, {self.uuid}, {self.departament_id})'


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(254), nullable=False)
    uuid = db.Column(db.String(36), unique=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f'User ({self.username}, {self.email}, {self.uuid})'
