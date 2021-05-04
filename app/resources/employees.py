from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from app import db
from app.models.models import Employee
from app.resources.auth import token_required
from app.schemas.employees import EmployeeSchema


class EmployeeListApi(Resource):
    employee_schema = EmployeeSchema()

    @token_required
    def get(self, uuid=None):
        if not uuid:
            return self.employee_schema.dump(Employee.query.all(), many=True), 200
        employee = Employee.query.filter_by(uuid=uuid).first_or_404()
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
        empl = Employee.query.filter_by(uuid=uuid).first_or_404()
        try:
            empl = self.employee_schema.load(request.json, instance=empl, session=db.session)
        except ValidationError as error:
            return {'message': str(error)}
        db.session.add(empl)
        db.session.commit()
        return self.employee_schema.dump(empl), 200

    def patch(self, uuid):
        empl = Employee.query.filter_by(uuid=uuid).first_or_404()
        empl_json = request.json
        first_name = empl_json.get('first_name')
        last_name = empl_json.get('last_name')
        salary = empl_json.get('salary')
        if first_name:
            empl.first_name = first_name
        elif last_name:
            empl.last_name = last_name
        elif salary:
            empl.salary = salary
        db.session.add(empl)
        db.session.commit()
        return {'message': 'OK'}, 200

    def delete(self, uuid):
        empl = Employee.query.filter_by(uuid=uuid).first_or_404()
        db.session.delete(empl)
        db.session.commit()
        return {'message': 'OK'}, 200