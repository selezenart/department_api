from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import Departament, Employee


class DepartamentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Departament
        load_instance = True


class EmployeeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
        load_instance = True
