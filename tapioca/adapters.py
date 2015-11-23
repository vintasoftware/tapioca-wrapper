# coding: utf-8

import json

from .tapioca import TapiocaInstantiator
from .exceptions import (
    ResponseProcessException, ClientError, ServerError)
from .serializers import SimpleSerializer
from .xml_helpers import (
    input_branches_to_xml_bytestring, xml_string_to_etree_elt_dict)


def generate_wrapper_from_adapter(adapter_class):
    return TapiocaInstantiator(adapter_class)


class TapiocaAdapter(object):
    serializer_class = SimpleSerializer

    def __init__(self, serializer_class=None, *args, **kwargs):
        if serializer_class:
            self.serializer = serializer_class()
        else:
            self.serializer = self.get_serializer()

    def _get_to_native_method(self, method_name, value):
        if not self.serializer:
            raise NotImplementedError("This client does not have a serializer")

        def to_native_wrapper():
            return self._value_to_native(method_name, value)

        return to_native_wrapper

    def _value_to_native(self, method_name, value):
        return self.serializer.deserialize(method_name, value)

    def get_serializer(self):
        if self.serializer_class:
            return self.serializer_class()

    def get_api_root(self, api_params):
        return self.api_root

    def fill_resource_template_url(self, template, params):
        return template.format(**params)

    def get_request_kwargs(self, api_params, *args, **kwargs):
        serialized = self.serialize_data(kwargs.get('data'))

        kwargs.update({
            'data': self.format_data_to_request(serialized),
        })
        return kwargs

    def process_response(self, response):
        if str(response.status_code).startswith('5'):
            raise ResponseProcessException(ServerError, None)

        data = self.response_to_native(response)

        if str(response.status_code).startswith('4'):
            raise ResponseProcessException(ClientError, data)

        return data

    def serialize_data(self, data):
        if self.serializer:
            return self.serializer.serialize(data)

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
        if response.content.strip():
            return response.json()


class XMLAdapterMixin(object):

    def get_request_kwargs(self, api_params, *args, **kwargs):
        arguments = super(XMLAdapterMixin, self).get_request_kwargs(
            api_params, *args, **kwargs)

        if 'headers' not in arguments:
            # allows user to override for formats like 'application/atom+xml'
            arguments['headers'] = {}
            arguments['headers']['Content-Type'] = 'application/xml'
        return arguments

    def format_data_to_request(self, data):
        if data:
            return input_branches_to_xml_bytestring(data)

    def response_to_native(self, response):
        if response.content.strip():
            if 'xml' in response.headers['content-type']:
                return {'xml': response.content,
                        'dict': xml_string_to_etree_elt_dict(response.content)}
            return {'text': response.text}
