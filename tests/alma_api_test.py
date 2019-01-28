import requests
from linked_account_update import settings

def test_linked_api_keys_exist():
    assert settings.LINKED_IZ_KEYS, "LINKED_IZ_KEYS does not exist, set in env or settings file"

def test_linked_api_keys_work():
    for k,v in settings.LINKED_IZ_KEYS.items():
        r = requests.get(settings.ALMA_SERVER + '/almaws/v1/users/operation/test',
            params={'apikey' : v})
        assert r.status_code == 200, "API request for inst {} failed".format(k)

def test_read_write_api_keys_work():

    for k,v in settings.IZ_READ_WRITE_KEYS.items():
        headers =  {'Authorization' : 'apikey ' + v}
        r = requests.post(settings.ALMA_SERVER + '/almaws/v1/users/operation/test',
            headers=headers)
        assert r.status_code == 200, "api key for {} could not be used to post to users api".format(k)
