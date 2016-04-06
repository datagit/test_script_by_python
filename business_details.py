from testapi_lib import *
from authenticate import *
from config import *
import json
import datetime
import sys

# edit the following
#id = '258|1052' # can have one or more biz ids separated by | (pipe)
id = '192672' 

api_url = base_api_url + '/sg/business/' + id
method = 'get'
output_file = 'z_business_details.json'
user_params = {
    #'search_type': 'food',
    #'status': 'closed',
	'include_timeslots': 'Y',
    #'per_page': 10,
    #'page': 1,
    #'term': 'Tian_Ji_Shu_Shi'
}
# end here

# manually override session_token if you want to
session_token = ''

arg1 = 0

if len(sys.argv) > 1:
    arg1 = sys.argv[1]

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

def main(argv):
    if not argv and int(argv) <=0:
        do_operation()
    else:
        total_time_request = 0
        argv = int(argv)
        for i in range(0, argv, 1):
            a = datetime.datetime.now()
            do_operation()
            b = datetime.datetime.now()
            total_time_request += (b-a).microseconds/1000

        print "Total time 10 requests: ", total_time_request/argv,'mili-seconds'

if __name__ == '__main__':
    main(arg1)
