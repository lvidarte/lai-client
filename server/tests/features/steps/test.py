# -*- coding: utf-8 -*-

import lettuce
import http


@lettuce.step(u'When I request the url "([^"]*)" with the method "([^"]*)"')
def request_the_url_with_method(step, url, method):
    lettuce.world.response = http.request(url, method)
    lettuce.world.response = http.json_loads_data(lettuce.world.response)

@lettuce.step(u'Then The response status code should be (\d+)')
def the_response_status_code_should_be(step, code):
    assert lettuce.world.response.status == int(code)

@lettuce.step(u'Then The response reason text should be "([^"]*)"')
def the_response_reason_text_should_be(step, text):
    assert lettuce.world.response.reason == text


@lettuce.step(u'Then I should get a json object')
def i_should_get_a_json_object(step):
    assert type(lettuce.world.response.data) == dict

