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
    else:
        return url


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


def json_loads_params(params):
    # Json encode for list, dict and tuple
    if type(params) == dict:
        for k, v in params:
            if type(v) in (list, dict, tuple):
                params[k] = json.dumps(v)
    return params


def json_loads_data(response):
    for k, v in response.headers:
        if k.lower() == 'content-type' and v.startswith('application/json'):
            response.data = json.loads(response.data)
    return response


def request_auto_json(url, method='GET', params=None, headers={}):
    response = request(url, method, json_loads_params(params), headers)
    return json_loads_data(response)

