# -*- coding: utf-8 -*-

import lettuce
import http


@lettuce.step(u'When I request the url "([^"]*)" with the method "([^"]*)"')
def request_the_url_with_method(step, url, method):
    lettuce.world.response = http.request2(url, method)

@lettuce.step(u'I see a list of documents')
def list_of_documents(step):
    assert type(lettuce.world.response.data) == list

