import requests
import pytest
from random import randint

endpoint = pytest.endpoint_assetusermanual
user_belonging_user_manual_ids = []
test_created_user_manual_ids = []


#
# HTTP GET
#
def test_get_all_with_token():
    global user_belonging_user_manual_ids
    resp = requests.get(endpoint, headers=pytest.headers)
    assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' + str(resp.status_code) + str(
        resp.json()['data'])
    response_data = resp.json()['data']
    for record in response_data['data']:
        assert record['is_account_user_id'] == pytest.decoded_token['id_account_user'], \
            'Data not matched! Expected is_account_user_id: ' + pytest.decoded_token['id_account_user'] \
            + ', but found : ' + str(record['is_account_user_id'])
        user_belonging_user_manual_ids.append(int(record['id']))


def test_get_all_without_token():
    resp = requests.get(endpoint)
    assert (resp.status_code == 401), 'Status code is not 401. Rather found : ' + str(resp.status_code) + str(
        resp.json()['data'])


def test_get_one_belonging_to_user():
    resp = requests.get(endpoint + str(user_belonging_user_manual_ids[-1]), headers=pytest.headers)

    assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' + str(resp.status_code)
    response_data = resp.json()['data'][0]
    assert int(response_data['id']) == user_belonging_user_manual_ids[-1], 'Data not matched! Expected location id: ' \
                                                                           + str(user_belonging_user_manual_ids[-1]) \
                                                                           + ', but found: ' \
                                                                           + str(response_data['id'])
    assert response_data['is_account_user_id'] == pytest.decoded_token['id_account_user'], \
        'Data not matched! Expected is_account_user_id: ' + pytest.decoded_token['id_account_user'] \
        + ', but found : ' + str(response_data['is_account_user_id'])


def test_get_one_sending_string_parameter():
    resp = requests.get(endpoint + 'anything', headers=pytest.headers)
    response_data = resp.json()
    assert (response_data['status'] == 204), 'Status code is not 204. Rather found : ' + str(response_data['status'])
    assert response_data['message'] == 'Solicitud exitosa pero sin resultados', \
        'Data not matched! Expected response message: ' + 'Solicitud exitosa pero sin resultados, but found: ' + \
        str(response_data['message'])


def test_get_one_not_belonging_to_user():
    resp = requests.get(endpoint + str(user_belonging_user_manual_ids[0] - 1), headers=pytest.headers)
    response_data = resp.json()
    assert (response_data['status'] == 204), 'Status code is not 204. Rather found : ' + str(response_data['status'])
    assert response_data['message'] == 'Solicitud exitosa pero sin resultados', \
        'Data not matched! Expected response message: ' + 'Solicitud exitosa pero sin resultados, but found: ' + \
        str(response_data['message'])


#
# HTTP POST
#
def test_post_create_sending_all_must_have_params():
    global test_created_user_manual_ids
    data = {'name': 'PYTEST asset user manual ' + str(randint(0, 1000)),
            'file_name': 'pytest_asset_user_manual.pdf'}
    resp = requests.post(endpoint, json=data, headers=pytest.headers)
    response_data = resp.json()['data']
    assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' \
                                      + str(resp.status_code)
    assert response_data['created'] is not None, 'User manual was not successfully created. \
        Expected a created ID number, but found : ' + str(response_data['created'])
    test_created_user_manual_ids.append(response_data['created'])


def test_post_create_sending_all_must_and_might_have_params():
    global test_created_user_manual_ids
    data = {'name': 'PYTEST asset user manual ' + str(randint(0, 1000)),
            'file_name': 'pytest_asset_user_manual.pdf',
            'file_url': 'http://myfakeurl.com/usermanual9203902'}
    resp = requests.post(endpoint, json=data, headers=pytest.headers)
    response_data = resp.json()['data']
    assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' \
                                      + str(resp.status_code)
    assert response_data['created'] is not None, 'User manual was not successfully created. \
        Expected a created ID number, but found : ' + str(response_data['created'])
    test_created_user_manual_ids.append(response_data['created'])


def test_post_create_without_sending_all_must_have_params():
    # missing 'name' param on data.
    data = {'file_name': 'pytest_asset_user_manual.pdf',
            'file_url': 'http://myfakeurl.com/usermanual9203902'}
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
    data = {'name': 'PYTEST asset user manual AFTER PUT ' + str(randint(0, 1000))}
    resp = requests.put(endpoint + str(test_created_user_manual_ids[0]), json=data, headers=pytest.headers)
    response_data = resp.json()['data']
    assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' \
                                      + str(resp.status_code)
    assert (response_data['updated'] == 1), 'User manual could not be modified. \
        Expected updated number: 1, but found : ' + str(response_data['updated'])


def test_put_modify_one_not_belonging_to_user():
    data = {'name': 'PYTEST asset user manual AFTER PUT ' + str(randint(0, 1000))}
    resp = requests.put(endpoint + str(user_belonging_user_manual_ids[0] - 1), json=data, headers=pytest.headers)
    response_data = resp.json()['data']
    assert (response_data['updated'] == 0), 'User manual was successfully modified, but it was not supposed to. \
        This user manual does not belong to the logged user. Expected updated ID: 0, but found : ' \
                                            + str(response_data['updated'])


#
# HTTP DELETE
#
# THIS HTTP METHOD IS BLOCKED BY THE MODEL ON API SO IT SHOULD NEVER DELETE A RECORD. FAILING TO DELETE IS JUST FINE.
def test_delete_belonging_to_user():
    if test_created_user_manual_ids:
        for ID in test_created_user_manual_ids:
            try:
                resp = requests.delete(endpoint + str(ID), headers=pytest.headers)
                response_data = resp.json()
                assert (response_data['status'] == 204), 'Status code is not 204. Rather found : ' \
                                                         + str(response_data['status'])
                assert response_data['message'] == 'Solicitud exitosa pero sin resultados', \
                    'Data not matched! Expected response message: ' + 'Solicitud exitosa pero sin resultados, but ' \
                                                                      'found: ' + str(response_data['message'])
            finally:
                connection = pytest.db_connection
                cursor = pytest.db_cursor
                delete_query = """Delete from is_asset_manual_user where id = """ + str(ID)
                cursor.execute(delete_query)
                connection.commit()


def test_delete_not_belonging_to_user():
    resp = requests.delete(endpoint + str(user_belonging_user_manual_ids[0] - 1), headers=pytest.headers)
    response_data = resp.json()
    assert (response_data['status'] == 204), 'Status code is not 204. Rather found : ' \
                                             + str(response_data['status'])
    assert response_data['message'] == 'Solicitud exitosa pero sin resultados', \
        'Data not matched! Expected response message: ' + 'Solicitud exitosa pero sin resultados, but found: ' + \
        str(response_data['message'])
