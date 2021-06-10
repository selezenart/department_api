from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from app import db
from app.schemas.departments import DepartamentSchema
from app.services.departament_service import DepartamentService


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

    def put(self, uuid):
        departament = DepartamentService.fetch_departament_by_uuid(db.session, uuid)
        try:
            departament = self.departament_schema.load(request.json, instance=departament, session=db.session)
        except ValidationError as error:
            return {'message': str(error)}
        db.session.add(departament)
        db.session.commit()
        return self.departament_schema.dump(departament), 200

    def patch(self, uuid):
        departament = DepartamentService.fetch_departament_by_uuid(db.session,uuid)
        departament_json = request.json
        title = departament_json.get('title')
        average_salary = departament_json.get('average_salary')
        employees = departament_json.get('employees')
        if title:
            departament.title = title
        elif average_salary:
            departament.average_salary = average_salary
        elif employees:
            departament.employees = employees
        db.session.add(departament)
        db.session.commit()
        return {'message': 'OK'}, 200

    def delete(self, uuid):
        departament = DepartamentService.fetch_departament_by_uuid(db.session, uuid)
        db.session.delete(departament)
        db.session.commit()
        return {'message': 'OK'}, 200
