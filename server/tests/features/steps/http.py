# -*- coding: utf-8 -*-

import json
import httplib
import urlparse
import urllib


class Response:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def get_full_url(url):
    if not url.startswith('http://'):
        return 'http://localhost:8888%s' % url


def request(url, method='GET', params=None, headers={}):
    url = get_full_url(url)
    url2 = urlparse.urlparse(url)
    conn = httplib.HTTPConnection(url2.netloc)

    if params:
        params = urllib.urlencode(params)
        headers["Content-type"] = "application/x-www-form-urlencoded"
        headers["Accept"] = "text/plain"

    conn.request(method, url2.path, params, headers)

    res = conn.getresponse()
    res_data = res.read()
    res_headers = res.getheaders()

    response = {'response': res,
                'status':   res.status,
                'reason':   res.reason,
                'headers':  res_headers,
                'data':     res_data}

    conn.close()
    return Response(**response)


def jsonify(params):
    # Json encode for list, dict and tuple
    if type(params) == dict:
        for k, v in params:
            if type(v) in (list, dict, tuple):
                params[str(k)] = json.dumps(v)
    return params


def request2(url, method='GET', params=None, headers={}):
    # Auto encode dict, list and tupe to json string
    response = request(url, method, jsonify(params), headers)

    # Auto load json
    for k, v in response.headers:
        if k.lower() == 'content-type' and v.startswith('application/json'):
            response.data = json.loads(response.data)

    return response
