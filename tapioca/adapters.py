# coding: utf-8

import json

from .tapioca import TapiocaInstantiator
from .exceptions import (
    ResponseProcessException, ClientError, ServerError)


def generate_wrapper_from_adapter(adapter_class):
    return TapiocaInstantiator(adapter_class)


class TapiocaAdapter(object):

    def get_api_root(self, api_params):
        return self.api_root

    def fill_resource_template_url(self, template, params):
        return template.format(**params)

    def get_request_kwargs(self, api_params, *args, **kwargs):
        kwargs.update({
            'data': self.format_data_to_request(kwargs.get('data')),
        })
        return kwargs

    def process_response(self, response):
        if str(response.status_code).startswith('5'):
            raise ResponseProcessException(ServerError, None)

        data = self.response_to_native(response)

        if str(response.status_code).startswith('4'):
            raise ResponseProcessException(ClientError, data)

        return data

    def format_data_to_request(self, data):
        raise NotImplementedError()

    def response_to_native(self, response):
        raise NotImplementedError()

    def get_iterator_list(self, response_data):
        raise NotImplementedError()

    def get_iterator_next_request_kwargs(self, iterator_request_kwargs,
                                         response_data, response):
        raise NotImplementedError()


class FormAdapterMixin(object):

    def format_data_to_request(self, data):
        return data

    def response_to_native(self, response):
        return {'text': response.text}


class JSONAdapterMixin(object):

    def get_request_kwargs(self, api_params, *args, **kwargs):
        arguments = super(JSONAdapterMixin, self).get_request_kwargs(
            api_params, *args, **kwargs)

        if 'headers' not in arguments:
            arguments['headers'] = {}
        arguments['headers']['Content-Type'] = 'application/json'
        return arguments

    def format_data_to_request(self, data):
        if data:
            return json.dumps(data)

    def response_to_native(self, response):
        return response.json()
