from testapi_lib import *
from config import *
import json

# Please update the variables with values which will be used for the test
# If you don't want to send a parameter, please set it to None
# consumer_key - Channel key generated when creating a channel in SSO
# consumer_secret - Secret generated when creating a channel in SSO
# access_token / access_token_secret -> generated via command line and requested from Devs

#Authentication info
auth_info = {
    #test
    'access_token': 'db4b50cdc47b1977fc6d74bdb64eda',
    'access_token_secret': '4f2f4314b2',
    'consumer_key': '2384fbb22b8a50369e429e52e5af24',
    'consumer_secret': '0848a8d894',
    #prod
    #'access_token': '3e3326ce819a8cc15147b2549baf64',
    #'access_token_secret': '7beab87725',
    #'consumer_key': '4a8cdee57f847f14972edf411f8fe7',
    #'consumer_secret': '8afa5ac8ac',
}


def authenticate():
    params = {
    }
    for k, v in auth_info.iteritems():
        if v is not None: params[k] = v

    r = post_data(params['consumer_secret'], auth_url, params)

    print "URL: ", r['url']
    print "Status: ", r['status']
    print "Headers: ", r['headers']
    print "JSON: ", r['message']

    j = json.loads(r['message'])

    f = file('z_authenticate.json', 'w')
    f.write(json.dumps(j, sort_keys=True, indent=4))
    f.close()

    return j

if __name__ == '__main__':
    authenticate()

