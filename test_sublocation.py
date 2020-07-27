import requests
import pytest
from random import randint

endpoint = pytest.endpoint_sublocation
user_belonging_location_id = None
user_belonging_sublocation_ids = []
test_created_sublocation_id = None


#
# HTTP GET
#
def test_get_all_with_token():
    global user_belonging_sublocation_ids
    global user_belonging_location_id
    resp = requests.get(endpoint, headers=pytest.headers)
    assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' + str(resp.status_code) + str(
        resp.json()['data'])
    response_data = resp.json()['data']
    user_belonging_location_id = response_data['data'][0]['is_account_location_id']
    for record in response_data['data']:
        assert record['is_account_user_id'] == pytest.decoded_token['id_account_user'], \
            'Data not matched! Expected is_account_user_id: ' + pytest.decoded_token['id_account_user'] \
            + ', but found : ' + str(record['is_account_user_id'])
        user_belonging_sublocation_ids.append(int(record['id']))


def test_get_all_without_token():
    resp = requests.get(endpoint)
    assert (resp.status_code == 401), 'Status code is not 401. Rather found : ' + str(resp.status_code) + str(
        resp.json()['data'])


def test_get_one_belonging_to_user():
    resp = requests.get(endpoint + str(user_belonging_sublocation_ids[-1]), headers=pytest.headers)

    assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' + str(resp.status_code)
    response_data = resp.json()['data'][0]
    assert int(response_data['id']) == user_belonging_sublocation_ids[-1], 'Data not matched! Expected sublocation id: ' \
                                                                           + str(user_belonging_sublocation_ids[-1]) \
                                                                           + ', but found: ' \
                                                                           + str(response_data['id'])
    assert response_data['is_account_user_id'] == pytest.decoded_token['id_account_user'], \
        'Data not matched! Expected is_account_user_id: ' + pytest.decoded_token['id_account_user'] \
        + ', but found : ' + str(response_data['is_account_user_id'])


def test_get_one_not_belonging_to_user():
    resp = requests.get(endpoint + str(user_belonging_sublocation_ids[0] - 1), headers=pytest.headers)
    response_data = resp.json()
    assert (response_data['status'] == 204), 'Status code is not 204. Rather found : ' + str(response_data['status'])
    assert response_data['message'] == 'Solicitud exitosa pero sin resultados', \
        'Data not matched! Expected response message: ' + 'Solicitud exitosa pero sin resultados, but found: ' + \
        str(response_data['message'])


#
# HTTP POST
#
def test_post_create_unique_name():
    global test_created_sublocation_id
    data = {'name': 'PYTEST sublocation',
            'description': 'This is a test sublocation created by PYTEST and should be deleted immediately',
            'is_account_location_id': str(user_belonging_location_id)}
    resp = requests.post(endpoint, json=data, headers=pytest.headers)
    response_data = resp.json()['data']
    assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' \
                                      + str(resp.status_code)
    assert response_data['created'] is not None, 'Sublocation was not successfully created. \
        Expected a created ID number, but found : ' + str(response_data['created'])
    test_created_sublocation_id = response_data['created']


def test_post_create_repeated_name():
    data = {'name': 'PYTEST sublocation',
            'description': 'This is a test sublocation created by PYTEST and should be deleted immediately',
            'is_account_location_id': str(user_belonging_location_id)}
    resp = requests.post(endpoint, json=data, headers=pytest.headers)
    response_data = resp.json()['data']
    assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' \
                                      + str(resp.status_code)
    assert response_data['created'] is None, 'Sublocation was successfully created but it was not supposed to. \
        The same sublocation name is already on users Database. Expected None created ID, but found : ' \
                                             + str(response_data['created'])


def test_post_create_using_location_id_that_does_not_belong_to_user():
    data = {'name': 'PYTEST sublocation',
            'description': 'This is a test sublocation created by PYTEST and should be deleted immediately',
            'is_account_location_id': str(int(user_belonging_location_id)-1)}
    resp = requests.post(endpoint, json=data, headers=pytest.headers)
    response_data = resp.json()['data']
    assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' \
                                      + str(resp.status_code)
    assert response_data['created'] is None, 'Sublocation was successfully created but it was not supposed to. \
        The same sublocation name is already on users Database. Expected None created ID, but found : ' \
                                             + str(response_data['created'])


def test_post_create_without_sending_all_must_have_params():
    # missing 'is_account_location_id' param on data.
    data = {'name': 'PYTEST Sublocation',
            'description': 'This is a test sublocation created by PYTEST and should be deleted immediately'}
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
    data = {'name': 'PYTEST sublocation after PUT ' + str(randint(0, 1000)),
            'description': 'This test sublocation was modified by PUT TEST method'}
    resp = requests.put(endpoint + str(test_created_sublocation_id), json=data, headers=pytest.headers)
    response_data = resp.json()['data']
    assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' \
                                      + str(resp.status_code)
    assert (response_data['updated'] == 1), 'Sublocation could not be modified. \
        Expected updated number: 1, but found : ' + str(response_data['updated'])


def test_put_modify_one_not_belonging_to_user():
    data = {'name': 'PYTEST sublocation after PUT',
            'description': 'This test sublocation was modified by PUT TEST method'}
    resp = requests.put(endpoint + str(user_belonging_sublocation_ids[0] - 1),
                        json=data,
                        headers=pytest.headers)
    response_data = resp.json()['data']
    assert (response_data['updated'] == 0), 'Sublocation was successfully modified, but it was not supposed to. \
        This sublocation does not belong to the logged user. Expected None updated ID, but found : ' \
                                            + str(response_data['updated'])


#
# HTTP DELETE
#
def test_delete_one_belonging_to_user():
    if test_created_sublocation_id is not None:
        try:
            resp = requests.delete(endpoint + str(test_created_sublocation_id), headers=pytest.headers)
            response_data = resp.json()['data']
            assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' \
                                              + str(resp.status_code)
            assert response_data['deleted'] == 1, 'Sublocation could not be deleted. Expected 1, but found : ' \
                                                  + str(response_data['deleted'])
        finally:
            connection = pytest.db_connection
            cursor = pytest.db_cursor
            delete_query = """Delete from is_account_sublocation where id = """ + str(test_created_sublocation_id)
            cursor.execute(delete_query)
            connection.commit()


def test_delete_one_not_belonging_to_user():
    resp = requests.delete(endpoint + str(user_belonging_sublocation_ids[0] - 1), headers=pytest.headers)
    response_data = resp.json()['data']
    assert (response_data['deleted'] == 404), 'Status code is not 404. Rather found : ' \
                                              + str(resp.status_code)
    assert response_data['message'] == 'Eliminación fallida por validación', 'Sublocation could not be deleted. ' \
                                                                             'Expected Eliminación fallida por ' \
                                                                             'validación, but found : ' \
                                                                             + str(response_data['deleted'])
