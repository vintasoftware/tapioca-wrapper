# coding: utf-8

from tapioca import (TapiocaClient, TapiocaAdapter)


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
        'docs': 'http://www.test.com/resource'
    }
}


class TestClientAdapter(TapiocaAdapter):
    api_root = 'https://api.test.com'
    resource_mapping = RESOURCE_MAPPING

    def get_request_kwargs(self, api_params):
        return {}

    def get_iterator_list(self, response_data):
        return response_data['data']

    def get_iterator_next_request_kwargs(self,
            iterator_request_kwargs, response_data):
        paging = response_data.get('paging')
        if not paging:
            return
        url = paging.get('next')

        if url:
            return {'url': url}


TestTapiocaClient = TapiocaClient(TestClientAdapter())
