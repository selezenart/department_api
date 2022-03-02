from app.models.models import Departament
from app.services.employee_service import EmployeeService


class DepartamentService:
    @staticmethod
    def fetch_all_departments(session):
        return session.query(Departament)

    @classmethod
    def fetch_departament_by_uuid(cls, session, uuid):
        return cls.fetch_all_departments(session).filter_by(uuid=uuid).first_or_404()

    @staticmethod
    def add_employee_to_departament(session, employee_uuid, departament_uuid):
        departament = DepartamentService.fetch_departament_by_uuid(session, departament_uuid)
        employee = EmployeeService.fetch_employee_by_uuid(session, employee_uuid)
        if departament and employee:
            if employee.departament_id:
                old_department = DepartamentService.fetch_departament_by_uuid(session, employee.departament_id)
                old_department.remove_employee(employee)
            departament.add_employee(employee)
            employee.change_departament(departament_uuid)

    @staticmethod
    def remove_employee_from_departament(session, employee_uuid, departament_uuid):
        departament = DepartamentService.fetch_departament_by_uuid(session, departament_uuid)
        employee = EmployeeService.fetch_employee_by_uuid(session, employee_uuid)
        if departament and employee:
            employees = EmployeeService.fetch_employees_from_departament_by_uuid(session, departament_uuid)
            if employees and employees.filter_by(uuid=employee_uuid).first():
                departament.remove_employee(employee)
                employee.change_departament()
