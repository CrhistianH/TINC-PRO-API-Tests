import requests
import pytest
from random import randint

endpoint = pytest.endpoint_userprofile
user_belonging_user_profile_id = int


#
# HTTP GET
#
def test_get_all_with_token():
    global user_belonging_user_profile_id
    resp = requests.get(endpoint, headers=pytest.headers)
    assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' + str(resp.status_code) + str(
        resp.json()['data'])
    response_data = resp.json()['data']['data'][0]
    assert response_data['id'] == pytest.decoded_token['id_user'], \
        'Data not matched! Expected id: ' + pytest.decoded_token['id_user'] \
        + ', but found : ' + str(response_data['id'])
    user_belonging_user_profile_id = int(response_data['id'])


def test_get_all_without_token():
    resp = requests.get(endpoint)
    assert (resp.status_code == 401), 'Status code is not 401. Rather found : ' + str(resp.status_code) + str(
        resp.json()['data'])


def test_get_one_belonging_to_user():
    resp = requests.get(endpoint + str(user_belonging_user_profile_id), headers=pytest.headers)

    assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' + str(resp.status_code) + str(
        resp.json()['data'])
    response_data = resp.json()['data'][0]
    assert response_data['id'] == pytest.decoded_token['id_user'], \
        'Data not matched! Expected id: ' + pytest.decoded_token['id_user'] \
        + ', but found : ' + str(response_data['id'])


def test_get_one_sending_string_parameter():
    resp = requests.get(endpoint + 'anything', headers=pytest.headers)
    response_data = resp.json()
    assert (response_data['status'] == 204), 'Status code is not 204. Rather found : ' + str(response_data['status'])
    assert response_data['message'] == 'Solicitud exitosa pero sin resultados', \
        'Data not matched! Expected response message: ' + 'Solicitud exitosa pero sin resultados, but found: ' + \
        str(response_data['message'])


def test_get_one_not_belonging_to_user():
    resp = requests.get(endpoint + str(user_belonging_user_profile_id - 1), headers=pytest.headers)
    response_data = resp.json()
    assert (response_data['status'] == 204), 'Status code is not 204. Rather found : ' + str(response_data['status'])
    assert response_data['message'] == 'Solicitud exitosa pero sin resultados', \
        'Data not matched! Expected response message: ' + 'Solicitud exitosa pero sin resultados, but found: ' + \
        str(response_data['message'])


#
# HTTP POST
#
# POST ACTION SHOULD BE BLOCKED ON THE MODEL, AS THE ENDPOINT AUTH/SIGNING IS THE ONE THAT SHOULD BE POSTING TO IT ONLY.
# THEREFORE, ALL OF THE FOLLOWING POST TESTS SHOULD NOT CREATE ANY ROW ON THE TABLE.
def test_post_create_sending_all_must_have_params():
    data = {'full_name': 'PYTEST user profile with only must have params',
            'email': 'pytest@pytest.com',
            'password': 'mypersonalpassword123'}
    resp = requests.post(endpoint, json=data, headers=pytest.headers)
    response_data = resp.json()
    assert (response_data['status'] == 204), 'Status code is not 204. Rather found : ' \
                                             + str(response_data['status'])
    assert response_data['message'] == 'Solicitud exitosa pero sin resultados', \
        'Data not matched! Expected response message: ' + 'Solicitud exitosa pero sin resultados, but ' \
                                                          'found: ' + str(response_data['message'])


def test_post_create_sending_all_must_and_might_have_params():
    data = {'full_name': 'PYTEST user profile with only must have params',
            'email': 'pytest@pytest.com',
            'password': 'mypersonalpassword123',
            'job_title': 'PYTEST engineer',
            'is_user_scholarship_cat_id': '3',
            'admission_date': '2019/12/12',
            'educational_program': 'PYTEST educational program',
            'raw_salary': '123.99',
            'school_name': 'PYTEST university',
            'week_hours': '45',
            'gc_background_picture_cat_id': '2',
            'profile_picture': 'https://fakepictureurl.com/picture93',
            'first_log': '0',
            'password_reset_code': 'jsiapdfpa90320',
            'activation_code': 'ajspdiaj903032',
            'terms_accepted': '0',
            'is_user_role_cat_id': '1'}
    resp = requests.post(endpoint, json=data, headers=pytest.headers)
    response_data = resp.json()
    assert (response_data['status'] == 204), 'Status code is not 204. Rather found : ' \
                                             + str(response_data['status'])
    assert response_data['message'] == 'Solicitud exitosa pero sin resultados', \
        'Data not matched! Expected response message: ' + 'Solicitud exitosa pero sin resultados, but ' \
                                                          'found: ' + str(response_data['message'])


def test_post_create_without_sending_all_must_have_params():
    # missing 'email' param on data.
    data = {'full_name': 'PYTEST user profile with only must have params'}
    resp = requests.post(endpoint, json=data, headers=pytest.headers)
    response_data = resp.json()
    assert (response_data['status'] == 204), 'Status code is not 204. Rather found : ' \
                                             + str(response_data['status'])
    assert response_data['message'] == 'Solicitud exitosa pero sin resultados', \
        'Data not matched! Expected response message: ' + 'Solicitud exitosa pero sin resultados, but ' \
                                                          'found: ' + str(response_data['message'])


#
# HTTP PUT
#
def test_put_modify_one_belonging_to_user():
    data = {'full_name': 'PYTEST full name after PUT ' + str(randint(0, 1000)),
            'job_title': 'PYTEST engineer ' + str(randint(0, 1000)),
            'is_user_scholarship_cat_id': '3',
            'admission_date': '2019/12/12',
            'educational_program': 'PYTEST educational program ' + str(randint(0, 1000)),
            'raw_salary': '123.99',
            'school_name': 'PYTEST university ' + str(randint(0, 1000)),
            'week_hours': str(randint(0, 60)),
            'gc_background_picture_cat_id': '2',
            'profile_picture': 'https://fakepictureurl.com/picture ' + str(randint(0, 1000)),
            'is_user_role_cat_id': '2'}
    resp = requests.put(endpoint + str(user_belonging_user_profile_id), json=data, headers=pytest.headers)
    response_data = resp.json()['data']
    assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' \
                                      + str(resp.status_code)
    assert (response_data['updated'] == 1), 'User profile could not be modified. \
        Expected updated number: 1, but found : ' + str(response_data['updated'])


def test_put_modify_one_not_belonging_to_user():
    data = {'full_name': 'PYTEST full name after PUT ' + str(randint(0, 1000)),
            'job_title': 'PYTEST engineer ' + str(randint(0, 1000)),
            'is_user_scholarship_cat_id': '3',
            'admission_date': '2019/12/12',
            'educational_program': 'PYTEST educational program ' + str(randint(0, 1000)),
            'raw_salary': '123.99',
            'school_name': 'PYTEST university ' + str(randint(0, 1000)),
            'week_hours': str(randint(0, 60)),
            'gc_background_picture_cat_id': '2',
            'profile_picture': 'https://fakepictureurl.com/picture ' + str(randint(0, 1000)),
            'is_user_role_cat_id': '2'}
    resp = requests.put(endpoint + str(user_belonging_user_profile_id - 1), json=data, headers=pytest.headers)
    response_data = resp.json()['data']
    assert (response_data['updated'] == 0), 'User profile was successfully modified, but it was not supposed to. \
        This user profile does not belong to the logged user. Expected updated ID: 0, but found : ' \
                                            + str(response_data['updated'])


#
# HTTP DELETE
#
def test_delete_belonging_to_user():
    resp = requests.delete(endpoint + str(user_belonging_user_profile_id), headers=pytest.headers)
    response_data = resp.json()['data']
    assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' \
                                      + str(resp.status_code)
    assert response_data['deleted'] == 1, 'Location could not be deleted. Expected 1, but found : ' \
                                          + str(response_data['deleted'])
    connection = pytest.db_connection
    cursor = pytest.db_cursor
    delete_query = """UPDATE is_user_profile SET is_active=1 WHERE id = """ + str(user_belonging_user_profile_id)
    cursor.execute(delete_query)
    connection.commit()


def test_delete_not_belonging_to_user():
    resp = requests.delete(endpoint + str(user_belonging_user_profile_id - 1), headers=pytest.headers)
    response_data = resp.json()['data']
    assert response_data['message'] == 'Eliminación fallida por validación', \
        'Data not matched! Expected response message: ' + 'Eliminación fallida por validación, but found: ' + \
        str(response_data['message'])
    assert (response_data['deleted'] == 404), 'User profile was successfully deleted, but it was not supposed to. \
        This user profile does not belong to the logged user. Expected deleted code: 404, but found : ' \
                                            + str(response_data['deleted'])
