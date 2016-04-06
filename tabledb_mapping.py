from testapi_lib import *
from authenticate import *
from config import *
import json

# edit the following
api_url = base_api_url + '/tabledb'
method = 'get'
output_file = 'z_tabledb_mapping.json'
user_params = {
    'business_id': '42273,42399', # one or more business ids separated by comma
    'restaurant_id': '4ef93caf3467c7fc0b000000,52297e9c74099f140b8b459e' # one or more restaurant ids separated by comma
}
# end here

# manually override session_token if you want to
session_token = ''

def  do_operation():
    global session_token
    if not session_token:
        res = authenticate()
        session_token = res['data']['session_token']
    params = {
        'session_token': session_token
    }
    for k,v in user_params.iteritems():
        if v is not None: params[k] = v

    r = send_data(method, auth_info['consumer_secret'], api_url, params)

    print "URL: ", r['url']
    print "Status: ", r['status']
    print "Headers: ", r['headers']
    print "JSON: ", r['message']

    j = json.loads(r['message'])

    f = file(output_file, 'w')
    f.write(json.dumps(j, sort_keys=True, indent=4))
    f.close()

    return j

if __name__ == '__main__':
   do_operation()
