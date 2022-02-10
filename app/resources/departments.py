from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
import json

from app import db
from app.schemas.departments import DepartamentSchema
from app.services.departament_service import DepartamentService
from app.models.models import Employee, Departament


class DepartamentListApi(Resource):
    departament_schema = DepartamentSchema()

    def get(self, uuid=None):
        if not uuid:
            return self.departament_schema.dump(DepartamentService.fetch_all_departments(db.session), many=True), 200
        departament = DepartamentService.fetch_departament_by_uuid(db.session, uuid)
        return self.departament_schema.dump(departament), 200

    def post(self):
        try:
            departament = self.departament_schema.load(request.json, session=db.session)
        except ValueError as error:
            return {'message': str(error)}, 400
        db.session.add(departament)
        db.session.commit()
        return self.departament_schema.dump(departament), 201

    def put(self, uuid): #"message": "{'employees': ['Invalid type.']}"
        departament = DepartamentService.fetch_departament_by_uuid(db.session, uuid)
        try:
            departament = self.departament_schema.load(request.json, instance=departament, session=db.session)
        except ValidationError as error:
            return {'message': str(error)}
        db.session.add(departament)
        db.session.commit()
        return self.departament_schema.dump(departament), 200

    def patch(self, uuid):
        departament = DepartamentService.fetch_departament_by_uuid(db.session, uuid)
        departament_json = request.json
        title = departament_json.get('title')
        employees = departament_json.get('employees')
        if title:
            departament.title = title
        elif employees:
            for employee in employees:
                departament.employees = []
                DepartamentService.add_employee_to_departament(db.session, employee_uuid=employee['uuid'], departament_uuid=uuid )
        db.session.add(departament)
        db.session.commit()
        return {'message': 'OK'}, 200

    def delete(self, uuid):
        departament = DepartamentService.fetch_departament_by_uuid(db.session, uuid)
        db.session.delete(departament)
        db.session.commit()
        return {'message': 'OK'}, 200
