import requests
import pytest
from random import randint

endpoint = pytest.endpoint_asset
user_belonging_asset_ids = []
test_created_asset_ids = []


#
# HTTP GET
#
def test_get_all_with_token():
    global user_belonging_asset_ids
    resp = requests.get(endpoint, headers=pytest.headers)
    assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' + str(resp.status_code) + str(
        resp.json()['data'])
    response_data = resp.json()['data']['data']
    for record in response_data:
        assert record['is_account_user_id'] == pytest.decoded_token['id_account_user'], \
            'Data not matched! Expected is_account_user_id: ' + pytest.decoded_token['id_account_user'] \
            + ', but found : ' + str(record['is_account_user_id'])
        user_belonging_asset_ids.append(int(record['id']))


def test_get_all_without_token():
    resp = requests.get(endpoint)
    assert (resp.status_code == 401), 'Status code is not 401. Rather found : ' + str(resp.status_code) + str(
        resp.json()['data'])


def test_get_one_belonging_to_user():
    resp = requests.get(endpoint + str(user_belonging_asset_ids[-1]), headers=pytest.headers)

    assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' + str(resp.status_code) + str(
        resp.json()['data'])
    response_data = resp.json()['data'][0]
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
    resp = requests.get(endpoint + str(user_belonging_asset_ids[0] - 1), headers=pytest.headers)
    response_data = resp.json()
    assert (response_data['status'] == 204), 'Status code is not 204. Rather found : ' + str(response_data['status'])
    assert response_data['message'] == 'Solicitud exitosa pero sin resultados', \
        'Data not matched! Expected response message: ' + 'Solicitud exitosa pero sin resultados, but found: ' + \
        str(response_data['message'])


#
# HTTP POST
#
def test_post_create_sending_all_must_have_params():
    global test_created_asset_ids
    data = {'is_asset_category_cat_id': '1',
            'is_asset_type_cat_id': '1',
            'is_asset_brand_cat_id': '1',
            'model': 'PYTEST MODEL SENDING JUST MUST HAVE PARAMS',
            'serial_number': 'PYTEST SN',
            'is_asset_status_cat_id': '1',
            'is_account_location_id': '314',
            'is_account_sublocation_id': '595',
            'is_asset_ownership_cat_id': '1'}
    resp = requests.post(endpoint, json=data, headers=pytest.headers)
    response_data = resp.json()
    assert (response_data['status'] == 200), 'Status code is not 200. Rather found : ' \
                                             + str(response_data['status'])
    assert response_data['data']['created'] is not None, 'Location was not successfully created. \
        Expected a created ID number, but found : ' + str(response_data['data']['created'])
    test_created_asset_ids.append(response_data['data']['created'])


def test_post_create_sending_all_must_and_might_have_params():
    global test_created_asset_ids
    data = {'is_asset_category_cat_id': '1',
            'is_asset_type_cat_id': '1',
            'is_asset_brand_cat_id': '1',
            'model': 'PYTEST MODEL SENDING ALL MUST AND MIGHT HAVE PARAMS',
            'serial_number': 'PYTEST SN',
            'is_asset_status_cat_id': '1',
            'is_account_location_id': '314',
            'is_account_sublocation_id': '595',
            'is_asset_ownership_cat_id': '1',
            'id_custom': 'MYID123',
            'is_asset_gmdn_cat_id': '1',
            'is_asset_criticality_cat_id': '1',
            'is_asset_risk_cat_id': '1',
            'is_user_profile_id': '205',
            'description': 'PYTEST description of the asset',
            'comments': 'PYTEST comments of the asset',
            'es_supplier_owner_id': '3',
            'es_supplier_seller_id': '3',
            'keeper': 'Pedro PYTEST',
            'is_asset_mprev_freq_cat_id': '1',
            'es_supplier_service_provider_id': '3',
            'last_mprev_date': '2019/11/12',
            'next_mprev_date': '2020/11/12',
            'is_asset_mprev_routine_cat_id': '1',
            'is_asset_verification_routine_cat_id': '1',
            'warranty_start_date': '2018/11/12',
            'warranty_end_date': '2021/11/12',
            'invoice_number': 'PYTEST930203',
            'purchase_date': '2018/11/12',
            'installation_date': '2018/11/12',
            'gc_currency_cat_id': '1',
            'purchase_price': '20999.99',
            'estimated_lifespan': '5',
            'software_version': 'V1.0.0',
            'operating_system': 'PYTEST OS',
            'firmware_version': 'PYTEST930.00',
            'invoice_url': 'http://myfakeurl.com/pytest',
            'warranty_sheet_url': 'http://myfakeurl.com/warrantysheet3980',
            'is_asset_manual_user_id': '7',
            'is_asset_manual_service_id': '8',
            'health_registry_url': 'http://myfakeurl.com/healthregystry9032',
            'import_request_url': 'http://myfakeurl.com/importrequest92032',
            'removal_date': '2019/12/12',
            'is_asset_removal_reason_cat_id': '1',
            'removal_comments': 'THIS WAS JUST FOR TESTING'}
    resp = requests.post(endpoint, json=data, headers=pytest.headers)
    response_data = resp.json()
    assert (response_data['status'] == 200), 'Status code is not 200. Rather found : ' \
                                             + str(response_data['status'])
    assert response_data['data']['created'] is not None, 'Location was not successfully created. \
        Expected a created ID number, but found : ' + str(response_data['data']['created'])
    test_created_asset_ids.append(response_data['data']['created'])


def test_post_create_without_sending_all_must_have_params():
    # missing 'model' param on data.
    data = {'is_asset_category_cat_id': '1',
            'is_asset_type_cat_id': '1',
            'is_asset_brand_cat_id': '1',
            'serial_number': 'PYTEST SN',
            'is_asset_status_cat_id': '1',
            'is_account_location_id': '314',
            'is_account_sublocation_id': '595',
            'is_asset_ownership_cat_id': '1'}
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
    data = {'model': 'PYTEST asset after PUT ' + str(randint(0, 1000)),
            'serial_number': 'PYTEST AFTER PUT MODIFICATION SN'}
    resp = requests.put(endpoint + str(test_created_asset_ids[0]), json=data, headers=pytest.headers)
    response_data = resp.json()['data']
    assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' \
                                      + str(resp.status_code)
    assert (response_data['updated'] == 1), 'Account could not be modified. \
        Expected updated number: 1, but found : ' + str(response_data['updated'])


def test_put_modify_one_not_belonging_to_user():
    data = {'model': 'PYTEST asset after PUT ' + str(randint(0, 1000)),
            'serial_number': 'PYTEST AFTER PUT MODIFICATION SN'}
    resp = requests.put(endpoint + str(user_belonging_asset_ids[0] - 1), json=data, headers=pytest.headers)
    response_data = resp.json()['data']
    assert (response_data['updated'] == 0), 'Account was successfully modified, but it was not supposed to. \
        This account does not belong to the logged user. Expected updated ID: 0, but found : ' \
                                            + str(response_data['updated'])


#
# HTTP DELETE
#
def test_delete_belonging_to_user():
    if test_created_asset_ids:
        for ID in test_created_asset_ids:
            try:
                resp = requests.delete(endpoint + str(ID), headers=pytest.headers)
                response_data = resp.json()['data']
                assert (resp.status_code == 200), 'Status code is not 200. Rather found : ' \
                                                  + str(resp.status_code)
                assert response_data['deleted'] == 1, 'Asset could not be deleted. Expected 1, but found : ' \
                                                      + str(response_data['deleted'])
            finally:
                connection = pytest.db_connection
                cursor = pytest.db_cursor
                delete_query = """Delete from is_asset_main where id = """ + str(ID)
                cursor.execute(delete_query)
                connection.commit()


def test_delete_not_belonging_to_user():
    resp = requests.delete(endpoint + str(user_belonging_asset_ids[0] - 1), headers=pytest.headers)
    response_data = resp.json()['data']
    assert (response_data['deleted'] == 404), 'Deleted id is not 404. Rather found : ' \
                                              + str(response_data['status'])
    assert response_data['message'] == 'Eliminación fallida por validación', \
        'Data not matched! Expected response message: ' + 'Eliminación fallida por validación, but found: ' + \
        str(response_data['message'])
