from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from app import db
from app.resources.auth import token_required
from app.schemas.employees import EmployeeSchema
from app.services.employee_service import EmployeeService
from app.services.departament_service import DepartamentService

class EmployeeListApi(Resource):
    employee_schema = EmployeeSchema()

    # @token_required
    def get(self, uuid=None):
        if not uuid:
            return self.employee_schema.dump(EmployeeService.fetch_all_employees(db.session), many=True), 200
        employee = EmployeeService.fetch_employee_by_uuid(db.session, uuid)
        return self.employee_schema.dump(employee), 200

    def post(self):
        try:
            empl = self.employee_schema.load(request.json, session=db.session)
        except ValueError as error:
            return {'message': str(error)}, 400
        db.session.add(empl)
        db.session.commit()
        return self.employee_schema.dump(empl), 201

    def put(self, uuid):
        empl = EmployeeService.fetch_employee_by_uuid(db.session, uuid)
        try:
            empl = self.employee_schema.load(request.json, instance=empl, session=db.session)
        except ValidationError as error:
            return {'message': str(error)}
        db.session.add(empl)
        db.session.commit()
        return self.employee_schema.dump(empl), 200

    def patch(self, uuid):
        empl = EmployeeService.fetch_employee_by_uuid(db.session, uuid)
        empl_json = request.json
        first_name = empl_json.get('first_name')
        last_name = empl_json.get('last_name')
        salary = empl_json.get('salary')
        departament_uuid = empl_json.get('departament_id')
        if first_name:
            empl.first_name = first_name
        elif last_name:
            empl.last_name = last_name
        elif salary:
            empl.salary = salary
            if empl.departament_id:
                departament = DepartamentService.fetch_departament_by_uuid(db.session, empl.departament_id)
                departament.update_avg_salary()
        elif departament_uuid:
            if empl.departament_id:
                departament = DepartamentService.fetch_departament_by_uuid(db.session, empl.departament_id)
                if departament is not 404:
                    departament.remove_employee(empl)
            new_departament = DepartamentService.fetch_departament_by_uuid(db.session, departament_uuid)
            new_departament.add_employee(empl)

        db.session.add(empl)
        db.session.commit()
        return {'message': 'OK'}, 200

    def delete(self, uuid):
        empl = EmployeeService.fetch_employee_by_uuid(db.session, uuid)
        db.session.delete(empl)
        db.session.commit()
        return {'message': 'OK'}, 200
