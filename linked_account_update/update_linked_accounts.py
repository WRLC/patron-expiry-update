import csv
import json
import os
import requests

# configuration form a file or from env
if os.environ.get('SETTINGS_FROM_ENV'):
    UPDATE_IZ_KEY = os.environ['UPDATE_IZ_KEY']
    LINKED_IZ_KEYS = os.environ['LINKED_IZ_KEYS']
    REPORT_FILE = os.environ['REPORT_FILE']
else:
    from settings import *

def alma_get(resource, apikey, params=None, fmt='json'):
    '''
    makes a generic alma api call, pass in a resource
    '''
    params = params or {}
    params['apikey'] = apikey
    params['format'] = fmt
    r = requests.get(resource, params=params) 
    r.raise_for_status()
    return r

def alma_put(resource, apikey, payload=None, params=None, fmt='json'):

    '''
    makes a generic post request to alma api.
    '''
    payload = payload or {}
    params = params or {}
    params['format'] = fmt
    headers =  {
        'Content-type': 'application/{fmt}'.format(fmt=fmt),
        'Authorization' : 'apikey ' + apikey,
    }
    r = requests.put(resource,
                     headers=headers,
                     params=params,
                     data=payload)
    r.raise_for_status()
    return r

def read_report_generator(report):
    with open(report, encoding='utf-8-sig') as fh:
        reader = csv.DictReader(fh, delimiter=',')
        for row in reader:
            yield row

def get_home_id_by_email(email, home_iz):
    r = alma_get(ALMA_SERVER + USERS_ROUTE,
                LINKED_IZ_KEYS[home_iz],
                params = {'q' : 'email~' + email})
    if r.json()['total_record_count'] == 1:
        return r.json()['user'][0]['primary_id']
    else:
        return False

def get_details_by_pid(home_pid, apikey):
    r = alma_get(ALMA_SERVER + USER_ROUTE.format(user_id=home_pid),
                apikey)
    try:
        return r.json()
    except:
        return False

def main():
    count_all_records = 0
    for row in read_report_generator(REPORT_FILE):
        linked_pid = row['Primary Identifier']
        linked_email = row['Preferred Email']
        home_iz = row['Linked From Institution Code']
        # request by email here
        try:
            home_pid = get_home_id_by_email(linked_email, home_iz)
        except:
            pass
        if home_pid:
            # if any of these fail, just move on and report that no update was done
            try:
                expiry_date = get_details_by_pid(home_pid, LINKED_IZ_KEYS[home_iz])['expiry_date']
                linked_account_details = get_details_by_pid(linked_pid, UPDATE_IZ_KEY)
                if linked_account_details['expiry_date'] == expiry_date:
                    print('No update required for {email}.'
                          ' Dates match at {date}'.format(email=linked_email, date=expiry_date))
                else:
                    print('Update required for {email}. '
                          'linked date is {ld}, '
                          'home date is {hd}'.format(email=linked_email,
                                                     ld=linked_account_details['expiry_date'],
                                                     hd=expiry_date))
                    linked_account_details['expiry_date'] = expiry_date
                    # post update
                    updated_account = alma_put(ALMA_SERVER + USER_ROUTE.format(user_id=linked_pid),
                                                UPDATE_IZ_KEY,
                                                payload=json.dumps(linked_account_details))
                    if updated_account.status_code == 200:
                        print("update successful")
                    else:
                        print("update failed for {}".format(linked_pid))
            except Exception as e:
                print(e.args[0])

        else:
            print("no pid for {}".format(linked_pid))
        count_all_records += 1



if __name__ == '__main__':
    main()
