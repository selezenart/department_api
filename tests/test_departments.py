import http
import json

from app import app


class FakeDepartament:
    title = 'Fake Title'


class TestDepartments:
    dep_uuid = []
    empl_uuid = []

    def test_departments_with_db(self):
        client = app.test_client()
        resp = client.get('/departments')
        assert resp.status_code == http.HTTPStatus.OK

    def test_create_departament_without_employees_with_db(self):
        client = app.test_client()
        data = {
            'title': 'Test Departament'
        }
        resp = client.post('/departments', data=json.dumps(data), content_type='application/json')
        self.dep_uuid.append(resp.json['uuid'])
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json['title'] == 'Test Departament'
        assert resp.json['employees'] == []
        assert resp.json['average_salary'] == 0.0

    def test_update_departament_with_db(self):
        client = app.test_client()
        url = f'/departments/{self.dep_uuid[0]}'
        data = {
            "title": "New Title"
        }
        resp = client.put(url, data=json.dumps(data), content_type="application/json")
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json['title'] == 'New Title'
        assert resp.json['employees'] == []
        assert resp.json['average_salary'] == 0.0

    def test_add_employee_to_departament(self):
        client = app.test_client()
        empl_data = {
            'first_name': 'First',
            'last_name': 'Employee',
            'salary': '1000'
        }
        empl_resp = client.post('/employees', data=json.dumps(empl_data), content_type='application/json')
        self.empl_uuid.append(empl_resp.json['uuid'])

        url = f'/departments/{self.dep_uuid[0]}'
        dep_data = {
            'employees':
                [
                        {
                            'uuid': self.empl_uuid[0],
                            'first_name': empl_data['first_name'],
                            'last_name': empl_data['last_name'],
                            'salary': empl_data['salary']
                        }

                ]
        }
        self.empl_uuid.append(empl_resp.json['uuid'])
        client.patch(url, data=json.dumps(dep_data), content_type='application/json')
        resp = client.get(url, data=json.dumps(dep_data), content_type='application/json')

        assert resp.json['title'] == 'New Title'
        assert resp.json['employees'][0]['uuid'] == self.empl_uuid[0]
        assert resp.json['average_salary'] == int(empl_data['salary'])

    def test_delete_departament_with_db(self):
        client = app.test_client()
        url = f'/departments/{self.dep_uuid[0]}'
        resp = client.delete(url)
        assert resp.status_code == http.HTTPStatus.OK

    def test_delete_departament_with_wrong_id_with_db(self):
        client = app.test_client()
        url = f'/departments/1'
        resp = client.delete(url)
        assert resp.status_code == http.HTTPStatus.NOT_FOUND


