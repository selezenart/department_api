import os

basedir = os.path.abspath(os.path.dirname(__file__))


def database_url():
    """Use DATABASE_URL when set (e.g. Heroku Postgres), otherwise the bundled SQLite file."""
    url = os.environ.get('DATABASE_URL')
    if not url:
        return 'sqlite:///' + os.path.join(basedir, 'data', 'app.db')
    # SQLAlchemy 1.4+ no longer accepts the legacy "postgres://" scheme.
    if url.startswith('postgres://'):
        url = url.replace('postgres://', 'postgresql://', 1)
    return url


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'very-secret-key'
    SQLALCHEMY_DATABASE_URI = database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
