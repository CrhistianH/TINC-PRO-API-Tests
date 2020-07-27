import requests
import pytest
from random import randint

endpoint = pytest.endpoint_location
user_belonging_location_ids = []
test_created_location_id = None


#
# HTTP GET
#
def test_get_all_with_token():
    global user_belonging_location_ids
    resp = requests.get(endpoint, headers=pytest.headers)
    assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' + str(resp.status_code) + str(
        resp.json()['data'])
    response_data = resp.json()['data']
    for record in response_data['data']:
        assert record['is_account_user_id'] == pytest.decoded_token['id_account_user'], \
            'Data not matched! Expected is_account_user_id: ' + pytest.decoded_token['id_account_user'] \
            + ', but found : ' + str(record['is_account_user_id'])
        user_belonging_location_ids.append(int(record['id']))


def test_get_all_without_token():
    resp = requests.get(endpoint)
    assert (resp.status_code == 401), 'Status code is not 401. Rather found : ' + str(resp.status_code) + str(
        resp.json()['data'])


def test_get_one_belonging_to_user():
    resp = requests.get(endpoint + str(user_belonging_location_ids[-1]), headers=pytest.headers)

    assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' + str(resp.status_code)
    response_data = resp.json()['data'][0]
    assert int(response_data['id']) == user_belonging_location_ids[-1], 'Data not matched! Expected location id: ' \
                                                                        + str(user_belonging_location_ids[-1]) \
                                                                        + ', but found: ' \
                                                                        + str(
        response_data['id'])
    assert response_data['is_account_user_id'] == pytest.decoded_token['id_account_user'], \
        'Data not matched! Expected is_account_user_id: ' + pytest.decoded_token['id_account_user'] \
        + ', but found : ' + str(response_data['is_account_user_id'])


def test_get_one_not_belonging_to_user():
    resp = requests.get(endpoint + str(user_belonging_location_ids[0] - 1), headers=pytest.headers)
    response_data = resp.json()
    assert (response_data['status'] == 204), 'Status code is not 204. Rather found : ' + str(response_data['status'])
    assert response_data['message'] == 'Solicitud exitosa pero sin resultados', \
        'Data not matched! Expected response message: ' + 'Solicitud exitosa pero sin resultados, but found: ' + \
        str(response_data['message'])


#
# HTTP POST
#
def test_post_create_unique_name():
    global test_created_location_id
    data = {'name': 'PYTEST location',
            'description': 'This is a test location created by PYTEST and should be deleted immediately'}
    resp = requests.post(endpoint, json=data, headers=pytest.headers)
    response_data = resp.json()['data']
    assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' \
                                      + str(resp.status_code)
    assert response_data['created'] is not None, 'Location was not successfully created. \
        Expected a created ID number, but found : ' + str(response_data['created'])
    test_created_location_id = response_data['created']


def test_post_create_repeated_name():
    data = {'name': 'PYTEST location',
            'description': 'This is a test location created by PYTEST and should be deleted immediately'}
    resp = requests.post(endpoint, json=data, headers=pytest.headers)
    response_data = resp.json()['data']
    assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' \
                                      + str(resp.status_code)
    assert response_data['created'] is None, 'Location was successfully created but it was not supposed to. \
        The same location name is already on users Database. Expected None created ID, but found : ' \
                                             + str(response_data['created'])


def test_post_create_without_sending_all_must_have_params():
    # missing 'name' param on data.
    data = {'description': 'This is a test location created by PYTEST and should be deleted immediately'}
    resp = requests.post(endpoint, json=data, headers=pytest.headers)
    response_data = resp.json()
    assert (response_data['status'] == 204), 'Status code is not 204. Rather found : ' + str(response_data['status'])
    assert response_data['message'] == 'Solicitud exitosa pero sin resultados', \
        'Data not matched! Expected response message: ' + 'Solicitud exitosa pero sin resultados, but found: ' + \
        str(response_data['message'])


#
# HTTP PUT
#
def test_put_modify_one_belonging_to_user():
    data = {'name': 'PYTEST location after PUT ' + str(randint(0, 1000)),
            'description': 'This test location was modified by PUT TEST method'}
    resp = requests.put(endpoint + str(test_created_location_id), json=data, headers=pytest.headers)
    response_data = resp.json()['data']
    assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' \
                                      + str(resp.status_code)
    assert (response_data['updated'] == 1), 'Location could not be modified. \
        Expected updated number: 1, but found : ' + str(response_data['updated'])


def test_put_modify_one_not_belonging_to_user():
    data = {'name': 'PYTEST location after PUT',
            'description': 'This test location was modified by PUT TEST method'}
    resp = requests.put(endpoint + str(user_belonging_location_ids[0] - 1), json=data, headers=pytest.headers)
    response_data = resp.json()['data']
    assert (response_data['updated'] == 0), 'Location was successfully modified, but it was not supposed to. \
        This location does not belong to the logged user. Expected None updated ID, but found : ' \
                                             + str(response_data['updated'])


#
# HTTP DELETE
#
def test_delete_one_belonging_to_user():
    if test_created_location_id is not None:
        try:
            resp = requests.delete(endpoint + str(test_created_location_id), headers=pytest.headers)
            response_data = resp.json()['data']
            assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' \
                                              + str(resp.status_code)
            assert response_data['deleted'] == 1, 'Location could not be deleted. Expected 1, but found : ' \
                                                  + str(response_data['deleted'])
        finally:
            connection = pytest.db_connection
            cursor = pytest.db_cursor
            delete_query = """Delete from is_account_location where id = """ + str(test_created_location_id)
            cursor.execute(delete_query)
            connection.commit()


def test_delete_one_not_belonging_to_user():
    resp = requests.delete(endpoint + str(user_belonging_location_ids[0] - 1), headers=pytest.headers)
    response_data = resp.json()['data']
    assert (response_data['deleted'] == 404), 'Status code is not 404. Rather found : ' \
                                              + str(resp.status_code)
    assert response_data['message'] == 'Eliminación fallida por validación', 'Location could not be deleted. ' \
                                                                             'Expected Eliminación fallida por ' \
                                                                             'validación, but found : ' \
                                                                             + str(response_data['deleted'])
