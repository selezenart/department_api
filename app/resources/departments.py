from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from app import db
from app.models.models import Departament
from app.schemas.departments import DepartamentSchema


class DepartamentListApi(Resource):
    departament_schema = DepartamentSchema()

    def get(self, uuid=None):
        if not uuid:
            return self.departament_schema.dump(Departament.query.all(), many=True), 200
        departament = Departament.query.filter_by(uuid=uuid).first_or_404()
        return self.departament_schema.dump(departament), 200

    def post(self):
        try:
            departament = self.departament_schema.load(request.json, session=db.session)
        except ValueError as error:
            return {'message': str(error)}, 400
        db.session.add(departament)
        db.session.commit()
        return self.departament_schema.dump(departament), 201

    def put(self, uuid):
        departament = Departament.query.filter_by(uuid=uuid).first_or_404()
        try:
            departament = self.departament_schema.load(request.json, instance=departament, session=db.session)
        except ValidationError as error:
            return {'message': str(error)}
        db.session.add(departament)
        db.session.commit()
        return self.departament_schema.dump(departament), 200

    def patch(self, uuid):
        departament = Departament.query.filter_by(uuid=uuid).first_or_404()
        departament_json = request.json
        title = departament_json.get('title')
        average_salary = departament_json.get('average_salary')
        if title:
            departament.title = title
        elif average_salary:
            departament.average_salary = average_salary
        db.session.add(departament)
        db.session.commit()
        return {'message': 'OK'}, 200

    def delete(self, uuid):
        departament = Departament.query.filter_by(uuid=uuid).first_or_404()
        db.session.delete(departament)
        db.session.commit()
        return {'message': 'OK'}, 200
