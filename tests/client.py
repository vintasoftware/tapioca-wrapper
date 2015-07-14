# coding: utf-8

from __future__ import unicode_literals

from tapioca import (
    TapiocaAdapter, generate_wrapper_from_adapter)


RESOURCE_MAPPING = {
    'test': {
        'resource': 'test/',
        'docs': 'http://www.test.com'
    },
    'user': {
        'resource': 'user/{id}/',
        'docs': 'http://www.test.com/user'
    },
    'resource': {
        'resource': 'resource/{number}/',
        'docs': 'http://www.test.com/resource',
        'spam': 'eggs',
        'foo': 'bar'
    },
}


class TestClientAdapter(TapiocaAdapter):
    api_root = 'https://api.test.com'
    resource_mapping = RESOURCE_MAPPING

    def get_request_kwargs(self, api_params):
        return {}

    def get_iterator_list(self, response_data):
        return response_data['data']

    def get_iterator_next_request_kwargs(self,
            iterator_request_kwargs, response_data, response):
        paging = response_data.get('paging')
        if not paging:
            return
        url = paging.get('next')

        if url:
            return {'url': url}


TestTapiocaClient = generate_wrapper_from_adapter(TestClientAdapter)
