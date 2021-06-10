from app.models.models import User


class UserService:
    @staticmethod
    def fetch_all_users(session):
        return session.query(User)

    @classmethod
    def fetch_user_by_username(cls, session, username):
        return cls.fetch_all_users(session).filter_by(username=username).first_or_404()

    @classmethod
    def fetch_user_by_uuid(cls, session, uuid):
        return cls.fetch_all_users(session).filter_by(uuid=uuid).first_or_404()

