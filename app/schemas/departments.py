from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from app.models.models import Departament


class DepartamentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Departament
        exclude = ['id']
        load_instance = True
        include_fk = True

    employees = Nested('EmployeeSchema', many=True, exclude=('departament_id', 'salary'))
