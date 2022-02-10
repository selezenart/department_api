import http
import json

from app import app


class TestEmployee:
    empl_uuid = []
    dep_uuid = []

    def test_employee_with_db(self):
        client = app.test_client()
        resp = client.get('/employees')
        assert resp.status_code == http.HTTPStatus.OK

    def test_create_employee_with_db(self):
        client = app.test_client()
        data = {
            'first_name': 'First',
            'last_name': 'Employee',
            'salary': '1000'
        }
        resp = client.post('/employees', data=json.dumps(data), content_type='application/json')
        self.empl_uuid.append(resp.json['uuid'])
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json['first_name'] == 'First'
        assert resp.json['last_name'] == 'Employee'
        assert resp.json['salary'] == 1000

    def test_update_employee_with_db(self):
        client = app.test_client()
        url = f'/employees/{self.empl_uuid[0]}'
        data = {
            'first_name': 'First',
            'last_name': 'Employee',
            'salary': '1100'
        }
        resp = client.put(url, data=json.dumps(data), content_type="application/json")
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json['first_name'] == 'First'
        assert resp.json['last_name'] == 'Employee'
        assert resp.json['salary'] == 1100

    def test_change_employee_departament_with_db(self):
        client = app.test_client()
        url = f'/employees/{self.empl_uuid[0]}'
        create_dep_data = {
            "title": "New Departament"
        }
        create_dep_resp = client.post('/departments', data=json.dumps(create_dep_data), content_type='application/json')
        self.dep_uuid.append(create_dep_resp.json['uuid'])
        data = {
            "departament_id": f"{self.dep_uuid[0]}"
        }
        resp = client.patch(url, data=json.dumps(data), content_type="application/json")
        assert resp.status_code == http.HTTPStatus.OK
        check_resp_employee = client.get(url)
        assert check_resp_employee.json['departament_id'] == self.dep_uuid[0]
        check_resp_departament = client.get(f'/departments/{self.dep_uuid[0]}')
        assert check_resp_departament.json['employees'][0]['uuid'] == self.empl_uuid[0]

    def test_delete_employee_with_db(self):
        client = app.test_client()
        url = f'/employees/{self.empl_uuid[0]}'
        resp = client.delete(url)
        assert resp.status_code == http.HTTPStatus.OK

    def test_delete_employee_with_wrong_id_with_db(self):
        client = app.test_client()
        url = f'/employees/1'
        resp = client.delete(url)
        assert resp.status_code == http.HTTPStatus.NOT_FOUND
