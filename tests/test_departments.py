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
            'title': 'Test Departament',
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
