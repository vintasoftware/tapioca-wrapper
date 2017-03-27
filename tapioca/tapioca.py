# coding: utf-8

from __future__ import unicode_literals

import copy

import requests
import webbrowser

import json
from collections import OrderedDict

from .exceptions import ResponseProcessException


class TapiocaInstantiator(object):

    def __init__(self, adapter_class):
        self.adapter_class = adapter_class

    def __call__(self, serializer_class=None, session=None, **kwargs):
        refresh_token_default = kwargs.pop('refresh_token_by_default', False)
        return TapiocaClient(
            self.adapter_class(serializer_class=serializer_class),
            api_params=kwargs, refresh_token_by_default=refresh_token_default,
            session=session)


class TapiocaClient(object):

    def __init__(self, api, data=None, response=None, request_kwargs=None,
                 api_params=None, resource=None, refresh_token_by_default=False,
                 refresh_data=None, session=None, *args, **kwargs):
        self._api = api
        self._data = data
        self._response = response
        self._api_params = api_params or {}
        self._request_kwargs = request_kwargs
        self._resource = resource
        self._refresh_token_default = refresh_token_by_default
        self._refresh_data = refresh_data
        self._session = session or requests.Session()

    def _instatiate_api(self):
        serializer_class = None
        if self._api.serializer:
            serializer_class = self._api.serializer.__class__
        return self._api.__class__(
            serializer_class=serializer_class)

    def _wrap_in_tapioca(self, data, *args, **kwargs):
        request_kwargs = kwargs.pop('request_kwargs', self._request_kwargs)
        return TapiocaClient(self._instatiate_api(), data=data,
                             api_params=self._api_params,
                             request_kwargs=request_kwargs,
                             refresh_token_by_default=self._refresh_token_default,
                             refresh_data=self._refresh_data,
                             session=self._session,
                             *args, **kwargs)

    def _wrap_in_tapioca_executor(self, data, *args, **kwargs):
        request_kwargs = kwargs.pop('request_kwargs', self._request_kwargs)
        return TapiocaClientExecutor(self._instatiate_api(), data=data,
                                     api_params=self._api_params,
                                     request_kwargs=request_kwargs,
                                     refresh_token_by_default=self._refresh_token_default,
                                     refresh_data=self._refresh_data,
                                     session=self._session,
                                     *args, **kwargs)

    def _get_doc(self):
        resources = copy.copy(self._resource)
        docs = ("Automatic generated __doc__ from resource_mapping.\n"
                "Resource: %s\n"
                "Docs: %s\n" % (resources.pop('resource', ''),
                                resources.pop('docs', '')))
        for key, value in sorted(resources.items()):
            docs += "%s: %s\n" % (key.title(), value)
        docs = docs.strip()
        return docs

    __doc__ = property(_get_doc)

    def __call__(self, *args, **kwargs):
        data = self._data

        url_params = self._api_params.get('default_url_params', {})
        url_params.update(kwargs)
        if self._resource and url_params:
            data = self._api.fill_resource_template_url(self._data, url_params)

        return self._wrap_in_tapioca_executor(data, resource=self._resource,
                                              response=self._response)
    """
    Convert a snake_case string in CamelCase.
    http://stackoverflow.com/questions/19053707/convert-snake-case-snake-case-to-lower-camel-case-lowercamelcase-in-python
    """
    def _to_camel_case(self, name):
        if isinstance(name, int):
            return name
        components = name.split('_')
        return components[0] + "".join(x.title() for x in components[1:])

    def _get_client_from_name(self, name):
        if (isinstance(self._data, list) and isinstance(name, int) or
                hasattr(self._data, '__iter__') and name in self._data):
            return self._wrap_in_tapioca(data=self._data[name])

        # if could not access, falback to resource mapping
        resource_mapping = self._api.resource_mapping
        if name in resource_mapping:
            resource = resource_mapping[name]
            api_root = self._api.get_api_root(self._api_params)

            url = api_root.rstrip('/') + '/' + resource['resource'].lstrip('/')
            return self._wrap_in_tapioca(url, resource=resource)

        return None

    def _get_client_from_name_or_fallback(self, name):
        client = self._get_client_from_name(name)
        if client is not None:
            return client

        camel_case_name = self._to_camel_case(name)
        client = self._get_client_from_name(camel_case_name)
        if client is not None:
            return client

        normal_camel_case_name = camel_case_name[0].upper()
        normal_camel_case_name += camel_case_name[1:]

        client = self._get_client_from_name(normal_camel_case_name)
        if client is not None:
            return client

        return None

    def __getattr__(self, name):
        ret = self._get_client_from_name_or_fallback(name)
        if ret is None:
            raise AttributeError(name)
        return ret

    def __getitem__(self, key):
        ret = self._get_client_from_name_or_fallback(key)
        if ret is None:
            raise KeyError(key)
        return ret

    def __dir__(self):
        if self._api and self._data is None:
            return [key for key in self._api.resource_mapping.keys()]

        if isinstance(self._data, dict):
            return self._data.keys()

        return []

    def __str__(self):
        if type(self._data) == OrderedDict:
            return ("<{} object, printing as dict:\n"
                    "{}>").format(
                self.__class__.__name__, json.dumps(self._data, indent=4))
        else:
            import pprint
            pp = pprint.PrettyPrinter(indent=4)
            return ("<{} object\n"
                    "{}>").format(
                self.__class__.__name__, pp.pformat(self._data))

    def _repr_pretty_(self, p, cycle):
        p.text(self.__str__())

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        return key in self._data


class TapiocaClientExecutor(TapiocaClient):

    def __init__(self, api, *args, **kwargs):
        super(TapiocaClientExecutor, self).__init__(api, *args, **kwargs)

    def __getitem__(self, key):
        raise Exception("This operation cannot be done on a" +
                        " TapiocaClientExecutor object")

    def __iter__(self):
        raise Exception("Cannot iterate over a TapiocaClientExecutor object")

    def __getattr__(self, name):
        if name.startswith('to_'):  # deserializing
            return self._api._get_to_native_method(name, self._data)
        return self._wrap_in_tapioca_executor(getattr(self._data, name))

    def __call__(self, *args, **kwargs):
        return self._wrap_in_tapioca(self._data.__call__(*args, **kwargs))

    @property
    def data(self):
        return self._data

    @property
    def response(self):
        if self._response is None:
            raise Exception("This instance has no response object")
        return self._response

    @property
    def status_code(self):
        return self.response.status_code

    @property
    def refresh_data(self):
        return self._refresh_data

    def _make_request(self, request_method, refresh_token=None, *args, **kwargs):
        if 'url' not in kwargs:
            kwargs['url'] = self._data

        request_kwargs = self._api.get_request_kwargs(
            self._api_params, request_method, *args, **kwargs)

        response = self._session.request(request_method, **request_kwargs)

        try:
            data = self._api.process_response(response)
        except ResponseProcessException as e:
            client = self._wrap_in_tapioca(e.data, response=response,
                                           request_kwargs=request_kwargs)
            tapioca_exception = e.tapioca_exception(client=client)

            should_refresh_token = (refresh_token is not False and
                                    self._refresh_token_default)
            auth_expired = self._api.is_authentication_expired(tapioca_exception)

            propagate_exception = True

            if should_refresh_token and auth_expired:
                self._refresh_data = self._api.refresh_authentication(self._api_params)
                if self._refresh_data:
                    propagate_exception = False
                    return self._make_request(request_method,
                                              refresh_token=False, *args, **kwargs)

            if propagate_exception:
                raise tapioca_exception

        return self._wrap_in_tapioca(data, response=response,
                                     request_kwargs=request_kwargs)

    def get(self, *args, **kwargs):
        return self._make_request('GET', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self._make_request('POST', *args, **kwargs)

    def put(self, *args, **kwargs):
        return self._make_request('PUT', *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self._make_request('PATCH', *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self._make_request('DELETE', *args, **kwargs)

    def _get_iterator_list(self):
        return self._api.get_iterator_list(self._data)

    def _get_iterator_next_request_kwargs(self):
        return self._api.get_iterator_next_request_kwargs(
            self._request_kwargs, self._data, self._response)

    def _reached_max_limits(self, page_count, item_count, max_pages,
                            max_items):
        reached_page_limit = max_pages is not None and max_pages <= page_count
        reached_item_limit = max_items is not None and max_items <= item_count
        return reached_page_limit or reached_item_limit

    def pages(self, max_pages=None, max_items=None, **kwargs):
        executor = self
        iterator_list = executor._get_iterator_list()
        page_count = 0
        item_count = 0

        while iterator_list:
            if self._reached_max_limits(page_count, item_count, max_pages,
                                        max_items):
                break
            for item in iterator_list:
                if self._reached_max_limits(page_count, item_count, max_pages,
                                            max_items):
                    break
                yield self._wrap_in_tapioca(item)
                item_count += 1

            page_count += 1

            next_request_kwargs = executor._get_iterator_next_request_kwargs()

            if not next_request_kwargs:
                break

            response = self.get(**next_request_kwargs)
            executor = response()
            iterator_list = executor._get_iterator_list()

    def open_docs(self):
        if not self._resource:
            raise KeyError()

        new = 2  # open in new tab
        webbrowser.open(self._resource['docs'], new=new)

    def open_in_browser(self):
        new = 2  # open in new tab
        webbrowser.open(self._data, new=new)

    def __dir__(self):
        methods = [m for m in TapiocaClientExecutor.__dict__.keys() if not m.startswith('_')]
        methods += [m for m in dir(self._api.serializer) if m.startswith('to_')]

        return methods
