import uuid

from app import db


class Departament(db.Model):
    __tablename = 'departments'
    id = db.Column(db.Integer(), primary_key=True)
    uuid = db.Column(db.String(36), unique=True)
    title = db.Column(db.String(120), nullable=False)
    average_salary = db.Column(db.Float(16), nullable=False)

    def __init__(self, title, average_salary):
        self.title = title
        self.average_salary = average_salary
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f'Departament({self.title}, {self.average_salary})'


class Employee(db.Model):
    __tablename = 'employee'
    id = db.Column(db.Integer(), primary_key=True)
    uuid = db.Column(db.String(36), unique=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    salary = db.Column(db.Float(16), nullable=False)

    def __init__(self, first_name, last_name, salary):
        self.first_name = first_name
        self.last_name = last_name
        self.salary = salary
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f'Employee({self.first_name},{self.last_name}, {self.salary}, {self.uuid})'

