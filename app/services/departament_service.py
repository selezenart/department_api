from app.models.models import Departament


class DepartamentService:
    @staticmethod
    def fetch_all_departments(session):
        return session.query(Departament)

    @classmethod
    def fetch_departament_by_uuid(cls, session, uuid):
        return cls.fetch_all_departments(session).filter_by(uuid=uuid).first_or_404()
