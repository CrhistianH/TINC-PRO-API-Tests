import requests
import pytest
from random import randint

endpoint = pytest.endpoint_account
user_belonging_account_id = int
test_created_account_ids = []


#
# HTTP GET
#
def test_get_all_with_token():
    global user_belonging_account_id
    resp = requests.get(endpoint, headers=pytest.headers)
    assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' + str(resp.status_code) + str(
        resp.json()['data'])
    response_data = resp.json()['data']['data'][0]
    assert response_data['id'] == pytest.decoded_token['id_account'], \
        'Data not matched! Expected id: ' + pytest.decoded_token['id_account'] \
        + ', but found : ' + str(response_data['id'])
    user_belonging_account_id = int(response_data['id'])


def test_get_all_without_token():
    resp = requests.get(endpoint)
    assert (resp.status_code == 401), 'Status code is not 401. Rather found : ' + str(resp.status_code) + str(
        resp.json()['data'])


def test_get_one_belonging_to_user():
    resp = requests.get(endpoint + str(user_belonging_account_id), headers=pytest.headers)

    assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' + str(resp.status_code) + str(
        resp.json()['data'])
    response_data = resp.json()['data'][0]
    assert response_data['id'] == pytest.decoded_token['id_account'], \
        'Data not matched! Expected id: ' + pytest.decoded_token['id_account'] \
        + ', but found : ' + str(response_data['id'])


def test_get_one_sending_string_parameter():
    resp = requests.get(endpoint + 'anything', headers=pytest.headers)
    response_data = resp.json()
    assert (response_data['status'] == 204), 'Status code is not 204. Rather found : ' + str(response_data['status'])
    assert response_data['message'] == 'Solicitud exitosa pero sin resultados', \
        'Data not matched! Expected response message: ' + 'Solicitud exitosa pero sin resultados, but found: ' + \
        str(response_data['message'])


def test_get_one_not_belonging_to_user():
    resp = requests.get(endpoint + str(user_belonging_account_id - 1), headers=pytest.headers)
    response_data = resp.json()
    assert (response_data['status'] == 204), 'Status code is not 204. Rather found : ' + str(response_data['status'])
    assert response_data['message'] == 'Solicitud exitosa pero sin resultados', \
        'Data not matched! Expected response message: ' + 'Solicitud exitosa pero sin resultados, but found: ' + \
        str(response_data['message'])


#
# HTTP POST
#
def test_post_create_sending_all_must_have_params():
    global test_created_account_ids
    data = {'name': 'PYTEST account only must have params',
            'is_account_sector_cat_id': '1',
            'gc_city_cat_id': '613',
            'gc_state_cat_id': '14',
            'gc_country_cat_id': '2',
            'gc_currency_cat_id': '2'}
    resp = requests.post(endpoint, json=data, headers=pytest.headers)
    response_data = resp.json()['data']
    assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' \
                                      + str(resp.status_code)
    assert response_data['created'] is not None, 'Location was not successfully created. \
        Expected a created ID number, but found : ' + str(response_data['created'])
    test_created_account_ids.append(response_data['created'])


def test_post_create_sending_all_must_and_might_have_params():
    global test_created_account_ids
    data = {'name': 'PYTEST account all must and might have params',
            'is_account_type_cat_id': '1',
            'is_account_sector_cat_id': '1',
            'gc_city_cat_id': '613',
            'gc_state_cat_id': '14',
            'gc_country_cat_id': '2',
            'gc_currency_cat_id': '2',
            'is_account_corporation_cat_id': '1',
            'contact_person': 'John Smith',
            'website_url': 'http://justtesting.com',
            'phone_number': '3333333333',
            'acronym': 'PYTEST',
            'legal_name': 'PY TEST SA DE CV',
            'gc_continent_cat_id': '1',
            'is_account_plan_cat_id': '1'}
    resp = requests.post(endpoint, json=data, headers=pytest.headers)
    response_data = resp.json()['data']
    assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' \
                                      + str(resp.status_code)
    assert response_data['created'] is not None, 'Location was not successfully created. \
        Expected a created ID number, but found : ' + str(response_data['created'])
    test_created_account_ids.append(response_data['created'])


def test_post_create_without_sending_all_must_have_params():
    # missing 'name' param on data.
    data = {'is_account_sector_cat_id': '1',
            'gc_city_cat_id': '613',
            'gc_state_cat_id': '14',
            'gc_country_cat_id': '2',
            'gc_currency_cat_id': '2'}
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
    data = {'name': 'PYTEST account after PUT ' + str(randint(0, 1000)),
            'contact_person': 'John Sanchez',
            'website_url': 'http://justtestingput.com',
            'phone_number': '0000000000',
            'acronym': 'PYTEST after PUT',
            'legal_name': 'PY TEST AFTER PUT SA DE CV'}
    resp = requests.put(endpoint + str(user_belonging_account_id), json=data, headers=pytest.headers)
    response_data = resp.json()['data']
    assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' \
                                      + str(resp.status_code)
    assert (response_data['updated'] == 1), 'Account could not be modified. \
        Expected updated number: 1, but found : ' + str(response_data['updated'])


def test_put_modify_one_not_belonging_to_user():
    data = {'name': 'PYTEST account after PUT',
            'contact_person': 'John Sanchez',
            'website_url': 'http://justtestingput.com',
            'phone_number': '0000000000',
            'acronym': 'PYTEST after PUT',
            'legal_name': 'PY TEST AFTER PUT SA DE CV'}
    resp = requests.put(endpoint + str(user_belonging_account_id - 1),
                        json=data,
                        headers=pytest.headers)
    response_data = resp.json()['data']
    assert (response_data['updated'] == 0), 'Account was successfully modified, but it was not supposed to. \
        This account does not belong to the logged user. Expected updated ID: 0, but found : ' \
                                             + str(response_data['updated'])


#
# HTTP DELETE
#
# THIS HTTP METHOD IS BLOCKED BY THE MODEL ON API SO IT SHOULD NEVER DELETE A RECORD. FAILING TO DELETE IS JUST FINE.
def test_delete_belonging_to_user():
    if test_created_account_ids:
        for ID in test_created_account_ids:
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
                delete_query = """Delete from is_account_main where id = """ + str(ID)
                cursor.execute(delete_query)
                connection.commit()


def test_delete_not_belonging_to_user():
    resp = requests.delete(endpoint + str(user_belonging_account_id - 1), headers=pytest.headers)
    response_data = resp.json()
    assert (response_data['status'] == 204), 'Status code is not 204. Rather found : ' \
                                             + str(response_data['status'])
    assert response_data['message'] == 'Solicitud exitosa pero sin resultados', \
        'Data not matched! Expected response message: ' + 'Solicitud exitosa pero sin resultados, but found: ' + \
        str(response_data['message'])
