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

    def test_change_employee_firstname_with_db(self):
        client = app.test_client()
        url = f'/employees/{self.empl_uuid[0]}'
        data = {
            'first_name': 'John'
        }
        resp = client.patch(url, data=json.dumps(data), content_type="application/json")
        assert resp.status_code == http.HTTPStatus.OK
        resp = client.get(url)
        assert resp.json['first_name'] == 'John'
        assert resp.json['last_name'] == 'Employee'
        assert resp.json['salary'] == 1100

    def test_change_employee_lastname_with_db(self):
        client = app.test_client()
        url = f'/employees/{self.empl_uuid[0]}'
        data = {
            'last_name': 'Smith',
        }
        resp = client.patch(url, data=json.dumps(data), content_type="application/json")
        assert resp.status_code == http.HTTPStatus.OK
        resp = client.get(url)
        assert resp.json['first_name'] == 'John'
        assert resp.json['last_name'] == 'Smith'
        assert resp.json['salary'] == 1100

    def test_change_employee_salary_in_departament_with_db(self):
        client = app.test_client()
        create_dep_data = {
            'title': 'New Department'
        }
        create_dep_resp = client.post('/departments', data=json.dumps(create_dep_data), content_type='application/json')
        self.dep_uuid.append(create_dep_resp.json['uuid'])
        url = f'/departments/{self.dep_uuid[0]}'
        dep_data = {
            'employees':
                [
                    {
                        'uuid': self.empl_uuid[0],
                        'first_name': 'John',
                        'last_name': 'Smith',
                        'salary': '1100'
                    }

                ]
        }
        resp = client.patch(url, data=json.dumps(dep_data), content_type="application/json")
        assert resp.status_code == http.HTTPStatus.OK
        data = {
            'salary': '2000',
        }
        url = f'/employees/{self.empl_uuid[0]}'
        resp = client.patch(url, data=json.dumps(data), content_type="application/json")
        assert resp.status_code == http.HTTPStatus.OK
        resp = client.get(url)
        assert resp.json['first_name'] == 'John'
        assert resp.json['last_name'] == 'Smith'
        assert resp.json['salary'] == 2000
        departament_uuid = resp.json['departament_id']
        resp = client.get(f'/departments/{departament_uuid}')
        assert resp.json['average_salary'] == 2000

    def test_change_employee_departament_with_db(self):
        client = app.test_client()
        url = f'/departments/'
        second_dep_data = {
            'title': 'Second Department'
        }
        resp = client.post(url, data=json.dumps(second_dep_data), content_type="application/json")
        self.dep_uuid.append(resp.json['uuid'])
        change_dep_data = {
            "departament_id": f'{self.dep_uuid[1]}'
        }
        url = f'/employees/{self.empl_uuid[0]}'
        resp = client.patch(url, data=json.dumps(change_dep_data), content_type="application/json")
        assert resp.status_code == http.HTTPStatus.OK
        check_resp_employee = client.get(f'employees/{self.empl_uuid[0]}')
        assert check_resp_employee.json['departament_id'] == self.dep_uuid[1]
        check_resp_departament = client.get(f'/departments/{self.dep_uuid[1]}')
        assert check_resp_departament.json['employees'][0]['uuid'] == self.empl_uuid[0]
        assert check_resp_departament.json['average_salary'] == 2000
        check_old_department = client.get(f'departments/{self.dep_uuid[0]}')
        assert check_old_department.json['average_salary'] == 0
        assert check_old_department.json['employees'] == []

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
