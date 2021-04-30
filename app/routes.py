from app import api
from app.resources.departments import DepartamentListApi
from app.resources.employees import EmployeeListApi
from app.resources.smoke import Smoke

api.add_resource(Smoke, '/smoke', strict_slashes=False)
api.add_resource(EmployeeListApi, '/employees', '/employees/<uuid>', strict_slashes=False)
api.add_resource(DepartamentListApi, '/departments', '/departments/<uuid>', strict_slashes=False)


