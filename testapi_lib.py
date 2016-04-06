import urllib, urllib2
from urlparse import urlparse
import hashlib
import copy

def sign(secret, url, params):
    parsed_url = urlparse(url)
    cleaned_url = parsed_url.path.replace('/api/web/app_dev.php/', '')
    hashed_str = secret + cleaned_url.replace('/', '')
    
    encoded_params = []
    for entry in urllib.urlencode(params, True).split('&'):
        pair = entry.split('=')
        if len(pair[1]) > 0:
            encoded_params.append(pair)

    encoded_params.sort(key=lambda x: x[0], reverse=False)
    for pair in encoded_params:
         hashed_str += pair[0] + pair[1]
         
    hashed_str = hashed_str
    print '\n', hashed_str  
    digest = hashlib.md5(hashed_str).hexdigest()
    print '\n', digest
    return digest

def send_data(httpMethod, secret, url, params):
    if httpMethod == 'get':
        return get_data(secret, url, params)
    elif httpMethod == 'post':
        return post_data(secret, url, params)
    elif httpMethod == 'put':
        return put_data(secret, url, params)
    elif httpMethod == 'delete':
        return delete_data(secret, url, params)

def post_data(secret, url, params):
    t_params = copy.deepcopy(params)
    sig = sign(secret, url, t_params)
    t_params['sig'] = sig
    encoded_params = urllib.urlencode(t_params, True)
    try:
        f = urllib2.urlopen(url, encoded_params)
    except urllib2.URLError, f:
        pass
    res = {
        'url': f.geturl(),
        'status': f.getcode(),
        'headers': copy.deepcopy(f.info().dict),
        'message': f.read()
    }
    f.close()
    return res

def get_data(secret, url, params):
    t_params = copy.deepcopy(params)
    sig = sign(secret, url, t_params)
    t_params['sig'] = sig
    encoded_params = urllib.urlencode(t_params, True)
    try:
        f = urllib2.urlopen(url + '?' + encoded_params)
    except urllib2.URLError, f:
        pass
    res = {
        'url': f.geturl(),
        'status': f.getcode(),
        'headers': copy.deepcopy(f.info().dict),
        'message': f.read()
    }
    f.close()
    return res

def put_data(secret, url, params):
    t_params = copy.deepcopy(params)
    sig = sign(secret, url, t_params)
    t_params['sig'] = sig
    encoded_params = urllib.urlencode(t_params, True)
    
    request = urllib2.Request(url, encoded_params)
    #request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    request.get_method = lambda: 'PUT'
    
    try:
        f = urllib2.urlopen(request)
    except urllib2.URLError, f:
        pass
    res = {
        'url': f.geturl(),
        'parameters': encoded_params,
        'status': f.getcode(),
        'headers': copy.deepcopy(f.info().dict),
        'message': f.read()
    }
    f.close()
    return res

def delete_data(secret, url, params):
    t_params = copy.deepcopy(params)
    sig = sign(secret, url, t_params)
    t_params['sig'] = sig
    encoded_params = urllib.urlencode(t_params, True)
    
    request = urllib2.Request(url + '?' + encoded_params)
    request.get_method = lambda: 'DELETE'
    
    try:
        f = urllib2.urlopen(request)
    except urllib2.URLError, f:
        pass
    res = {
        'url': f.geturl(),
        'parameters': encoded_params,
        'status': f.getcode(),
        'headers': copy.deepcopy(f.info().dict),
        'message': f.read()
    }
    f.close()
    return res
