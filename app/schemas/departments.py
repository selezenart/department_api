from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models.models import Departament


class DepartamentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Departament
        exclude = ['id']
        load_instance = True