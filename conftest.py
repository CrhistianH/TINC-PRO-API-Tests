import pytest
import jwt
import requests
import mysql.connector
from getpass import getpass


def endpoint_login_plugin():
    return 'http://localhost/TincLTE-Backend/auth/login/'
    
    
def endpoint_userprofile_plugin():
    return 'http://localhost/TincLTE-Backend/api/userprofile/'
    

def endpoint_account_plugin():
    return 'http://localhost/TincLTE-Backend/api/account/'
    

def endpoint_location_plugin():
    return 'http://localhost/TincLTE-Backend/api/location/'
    
    
def endpoint_sublocation_plugin():
    return 'http://localhost/TincLTE-Backend/api/sublocation/'


def endpoint_asset_plugin():
    return 'http://localhost/TincLTE-Backend/api/asset/'
    

def endpoint_assetservicemanual_plugin():
    return 'http://localhost/TincLTE-Backend/api/assetservicemanual/'
    

def endpoint_assetusermanual_plugin():
    return 'http://localhost/TincLTE-Backend/api/assetusermanual/'
    

def db_connection_plugin():
    return mysql.connector.connect(host='tinclitedevelopment.ctjmekakfpzf.us-east-1.rds.amazonaws.com',
                                         database='tinc_core_development',
                                         user='admin',
                                         password='Tinc2019*')


def db_cursor_plugin():
    return pytest.db_connection.cursor()
    
    
def email_plugin():
    return 'crhistianhigareda@gmail.com'
    # return input('\n\nEnter your TINC email address\n')

    
def password_plugin():
    return 'chester1'
    # return getpass('\nEnter your TINC password (input is not visible)\n')

    
def token_plugin():
    login_data = {'email': pytest.email,
                  'password': pytest.password}
    resp = requests.post(url=pytest.endpoint_login, json=login_data)
    returned_data = resp.json()
    assert (resp.status_code == 200), "Status code is not 200. Rather found : " + str(resp.status_code)
    return returned_data['token']


def headers_plugin():
    return {'Authorization': 'bearer ' + pytest.token}

    
def raw_decoded_token_plugin():
    return jwt.decode(pytest.token, verify=False, algorithms=['HS256'])

    
def decoded_token_plugin():
    return pytest.raw_decoded_token['data']

    
def pytest_configure():
    pytest.endpoint_login = endpoint_login_plugin()
    pytest.endpoint_userprofile = endpoint_userprofile_plugin()
    pytest.endpoint_account = endpoint_account_plugin()
    pytest.endpoint_location = endpoint_location_plugin()
    pytest.endpoint_sublocation = endpoint_sublocation_plugin()
    pytest.endpoint_asset = endpoint_asset_plugin()
    pytest.endpoint_assetservicemanual = endpoint_assetservicemanual_plugin()
    pytest.endpoint_assetusermanual = endpoint_assetusermanual_plugin()
    pytest.db_connection = db_connection_plugin()
    pytest.db_cursor = db_cursor_plugin()
    
    pytest.email = email_plugin()
    pytest.password = password_plugin()
    pytest.token = token_plugin()
    pytest.headers = headers_plugin()
    pytest.raw_decoded_token = raw_decoded_token_plugin()
    pytest.decoded_token = decoded_token_plugin()
    
    
def pytest_sessionfinish():
    if pytest.db_connection.is_connected():
        pytest.db_cursor.close()
        pytest.db_connection.close()