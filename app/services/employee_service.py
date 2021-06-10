from app.models.models import Employee


class EmployeeService:
    @staticmethod
    def fetch_all_employees(session):
        return session.query(Employee)

    @classmethod
    def fetch_employee_by_uuid(cls, session, uuid):
        return cls.fetch_all_employees(session).filter_by(uuid=uuid).first_or_404()

