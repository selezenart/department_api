from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models.models import User


class UsersSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ['id']
        load_instance = True
        load_only = ['password']
