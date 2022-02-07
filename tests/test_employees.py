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