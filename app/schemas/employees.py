from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models.models import Employee


class EmployeeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
        exclude = ['id']
        include_fk = True
        load_instance = True
