# coding: utf-8

from __future__ import unicode_literals

from tapioca.adapters import (
    TapiocaAdapter, JSONAdapterMixin,
    generate_wrapper_from_adapter)
from tapioca.serializers import SimpleSerializer


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


class TesterClientAdapter(JSONAdapterMixin, TapiocaAdapter):
    serializer_class = None
    api_root = 'https://api.test.com'
    resource_mapping = RESOURCE_MAPPING

    def get_iterator_list(self, response_data):
        return response_data['data']

    def get_iterator_next_request_kwargs(self, iterator_request_kwargs,
                                         response_data, response):
        paging = response_data.get('paging')
        if not paging:
            return
        url = paging.get('next')

        if url:
            return {'url': url}


TesterClient = generate_wrapper_from_adapter(TesterClientAdapter)


class SerializerClientAdapter(TesterClientAdapter):
    serializer_class = SimpleSerializer


SerializerClient = generate_wrapper_from_adapter(SerializerClientAdapter)


class TokenRefreshClientAdapter(TesterClientAdapter):

    def is_authentication_expired(self, exception, *args, **kwargs):
        return exception.status_code == 401

    def refresh_authentication(self, api_params, *args, **kwargs):
        api_params['token'] = 'new_token'


TokenRefreshClient = generate_wrapper_from_adapter(TokenRefreshClientAdapter)


class TokenRequesterClientAdapter(TesterClientAdapter):

    @classmethod
    def authorize_application(cls):
        return True

    @classmethod
    def request_token(cls):
        return True

    @classmethod
    def prompt_request_token(cls):
        return True

TokenRequesterClient = generate_wrapper_from_adapter(TokenRequesterClientAdapter)
