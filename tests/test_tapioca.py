# coding: utf-8

from __future__ import unicode_literals

import unittest
import responses
import arrow
import json
from decimal import Decimal

from tapioca.tapioca import TapiocaClient
from tapioca.serializers import SimpleSerializer
from tapioca.exceptions import ClientError

from tests.client import TesterClient, SerializerClient


class TestTapiocaClient(unittest.TestCase):

    def setUp(self):
        self.wrapper = TesterClient()

    def test_fill_url_template(self):
        expected_url = 'https://api.test.com/user/123/'

        resource = self.wrapper.user(id='123')

        self.assertEqual(resource.data, expected_url)

    def test_calling_len_on_tapioca_list(self):
        client = self.wrapper._wrap_in_tapioca([0, 1, 2])
        self.assertEqual(len(client), 3)

    def test_iterated_client_items_should_be_tapioca_instances(self):
        client = self.wrapper._wrap_in_tapioca([0, 1, 2])

        for item in client:
            self.assertTrue(isinstance(item, TapiocaClient))

    def test_iterated_client_items_should_contain_list_items(self):
        client = self.wrapper._wrap_in_tapioca([0, 1, 2])

        for i, item in enumerate(client):
            self.assertEqual(item().data, i)

    @responses.activate
    def test_in_operator(self):
        responses.add(responses.GET, self.wrapper.test().data,
                      body='{"data": 1, "other": 2}',
                      status=200,
                      content_type='application/json')

        response = self.wrapper.test().get()

        self.assertIn('data', response)
        self.assertIn('other', response)
        self.assertNotIn('wat', response)

    @responses.activate
    def test_trasnform_camelCase_in_snake_case(self):
        next_url = 'http://api.teste.com/next_batch'

        responses.add(responses.GET, self.wrapper.test().data,
                      body='{"data" :{"key_snake": "value", "camelCase": "data in camel case", "NormalCamelCase": "data in camel case"}, "paging": {"next": "%s"}}' % next_url,
                      status=200,
                      content_type='application/json')


        response = self.wrapper.test().get()

        self.assertEqual(response.data.key_snake().data, 'value')
        self.assertEqual(response.data.camel_case().data, 'data in camel case')
        self.assertEqual(response.data.normal_camel_case().data, 'data in camel case')



class TestTapiocaExecutor(unittest.TestCase):

    def setUp(self):
        self.wrapper = TesterClient()

    def test_resource_executor_data_should_be_composed_url(self):
        expected_url = 'https://api.test.com/test/'
        resource = self.wrapper.test()

        self.assertEqual(resource.data, expected_url)

    def test_docs(self):
        self.assertEqual(
            '\n'.join(self.wrapper.resource.__doc__.split('\n')[1:]),
            'Resource: ' + self.wrapper.resource._resource['resource'] + '\n'
            'Docs: ' + self.wrapper.resource._resource['docs'] + '\n'
            'Foo: ' + self.wrapper.resource._resource['foo'] + '\n'
            'Spam: ' + self.wrapper.resource._resource['spam'])

    def test_access_data_attributres_through_executor(self):
        client = self.wrapper._wrap_in_tapioca({'test': 'value'})

        items = client().items()

        self.assertTrue(isinstance(items, TapiocaClient))

        data = dict(items().data)

        self.assertEqual(data, {'test': 'value'})

    def test_is_possible_to_reverse_a_list_through_executor(self):
        client = self.wrapper._wrap_in_tapioca([0, 1, 2])
        client().reverse()
        self.assertEqual(client().data, [2, 1, 0])

    def test_cannot__getittem__(self):
        client = self.wrapper._wrap_in_tapioca([0, 1, 2])
        with self.assertRaises(Exception):
            client()[0]

    def test_cannot_iterate(self):
        client = self.wrapper._wrap_in_tapioca([0, 1, 2])
        with self.assertRaises(Exception):
            for item in client():
                pass

    def test_dir_call_returns_executor_methods(self):
        client = self.wrapper._wrap_in_tapioca([0, 1, 2])

        e_dir = dir(client())

        self.assertIn('data', e_dir)
        self.assertIn('response', e_dir)
        self.assertIn('get', e_dir)
        self.assertIn('post', e_dir)
        self.assertIn('pages', e_dir)
        self.assertIn('open_docs', e_dir)
        self.assertIn('open_in_browser', e_dir)

    @responses.activate
    def test_response_executor_object_has_a_response(self):
        next_url = 'http://api.teste.com/next_batch'

        responses.add(responses.GET, self.wrapper.test().data,
                      body='{"data": [{"key": "value"}], "paging": {"next": "%s"}}' % next_url,
                      status=200,
                      content_type='application/json')

        responses.add(responses.GET, next_url,
                      body='{"data": [{"key": "value"}], "paging": {"next": ""}}',
                      status=200,
                      content_type='application/json')

        response = self.wrapper.test().get()
        executor = response()

        executor.response

        executor._response = None

    def test_raises_error_if_executor_does_not_have_a_response_object(self):
        client = self.wrapper

        with self.assertRaises(Exception):
            client().response

    @responses.activate
    def test_response_executor_has_a_status_code(self):
        responses.add(responses.GET, self.wrapper.test().data,
                      body='{"data": {"key": "value"}}',
                      status=200,
                      content_type='application/json')

        response = self.wrapper.test().get()

        self.assertEqual(response().status_code, 200)


class TestTapiocaExecutorRequests(unittest.TestCase):

    def setUp(self):
        self.wrapper = TesterClient()

    def test_when_executor_has_no_response(self):
        with self.assertRaises(Exception) as context:
            self.wrapper.test().response

        exception = context.exception

        self.assertIn("has no response", str(exception))

    @responses.activate
    def test_get_request(self):
        responses.add(responses.GET, self.wrapper.test().data,
                      body='{"data": {"key": "value"}}',
                      status=200,
                      content_type='application/json')

        response = self.wrapper.test().get()

        self.assertEqual(response().data, {'data': {'key': 'value'}})

    @responses.activate
    def test_access_response_field(self):
        responses.add(responses.GET, self.wrapper.test().data,
                      body='{"data": {"key": "value"}}',
                      status=200,
                      content_type='application/json')

        response = self.wrapper.test().get()

        response_data = response.data()

        self.assertEqual(response_data.data, {'key': 'value'})

    @responses.activate
    def test_post_request(self):
        responses.add(responses.POST, self.wrapper.test().data,
                      body='{"data": {"key": "value"}}',
                      status=201,
                      content_type='application/json')

        response = self.wrapper.test().post()

        self.assertEqual(response().data, {'data': {'key': 'value'}})

    @responses.activate
    def test_token_expired_and_not_refresh_flag(self):
        responses.add(responses.POST, self.wrapper.test().data,
                      body='{"error": "Token expired"}',
                      status=401,
                      content_type='application/json')
        with self.assertRaises(ClientError) as context:
            response = self.wrapper.test().post()

    @responses.activate
    def test_token_expired_and_refresh_flag(self):
        self.first_call = True
        responses.add_callback(
          responses.POST, self.wrapper.test().data,
          callback=self.request_callback,
          content_type='application/json',
        )
        
        response = self.wrapper.test().post(True)

    def request_callback(self, request):
      if self.first_call:
        self.first_call = False
        return (401, {'content_type':'application/json'}, json.dumps('{"error": "Token expired"}'))
      else:
        self.first_call = None
        return (201, {'content_type':'application/json'}, json.dumps('{"error": "Token expired"}'))

    @responses.activate
    def test_put_request(self):
        responses.add(responses.PUT, self.wrapper.test().data,
                      body='{"data": {"key": "value"}}',
                      status=201,
                      content_type='application/json')

        response = self.wrapper.test().put()

        self.assertEqual(response().data, {'data': {'key': 'value'}})

    @responses.activate
    def test_patch_request(self):
        responses.add(responses.PATCH, self.wrapper.test().data,
                      body='{"data": {"key": "value"}}',
                      status=201,
                      content_type='application/json')

        response = self.wrapper.test().patch()

        self.assertEqual(response().data, {'data': {'key': 'value'}})

    @responses.activate
    def test_delete_request(self):
        responses.add(responses.DELETE, self.wrapper.test().data,
                      body='{"data": {"key": "value"}}',
                      status=201,
                      content_type='application/json')

        response = self.wrapper.test().delete()

        self.assertEqual(response().data, {'data': {'key': 'value'}})

    @responses.activate
    def test_simple_pages_iterator(self):
        next_url = 'http://api.teste.com/next_batch'

        responses.add(responses.GET, self.wrapper.test().data,
                      body='{"data": [{"key": "value"}], "paging": {"next": "%s"}}' % next_url,
                      status=200,
                      content_type='application/json')

        responses.add(responses.GET, next_url,
                      body='{"data": [{"key": "value"}], "paging": {"next": ""}}',
                      status=200,
                      content_type='application/json')

        response = self.wrapper.test().get()

        iterations_count = 0
        for item in response().pages():
            self.assertIn(item.key().data, 'value')
            iterations_count += 1

        self.assertEqual(iterations_count, 2)

    @responses.activate
    def test_simple_pages_with_max_items_iterator(self):
        next_url = 'http://api.teste.com/next_batch'

        responses.add(responses.GET, self.wrapper.test().data,
                      body='{"data": [{"key": "value"}], "paging": {"next": "%s"}}' % next_url,
                      status=200,
                      content_type='application/json')

        responses.add(responses.GET, next_url,
                      body='{"data": [{"key": "value"}, {"key": "value"}, {"key": "value"}], "paging": {"next": ""}}',
                      status=200,
                      content_type='application/json')

        response = self.wrapper.test().get()

        iterations_count = 0
        for item in response().pages(max_items=3, max_pages=2):
            self.assertIn(item.key().data, 'value')
            iterations_count += 1

        self.assertEqual(iterations_count, 3)

    @responses.activate
    def test_simple_pages_with_max_pages_iterator(self):
        next_url = 'http://api.teste.com/next_batch'

        responses.add(responses.GET, self.wrapper.test().data,
                      body='{"data": [{"key": "value"}], "paging": {"next": "%s"}}' % next_url,
                      status=200,
                      content_type='application/json')
        responses.add(responses.GET, next_url,
                      body='{"data": [{"key": "value"}, {"key": "value"}, {"key": "value"}], "paging": {"next": "%s"}}' % next_url,
                      status=200,
                      content_type='application/json')

        responses.add(responses.GET, next_url,
                      body='{"data": [{"key": "value"}, {"key": "value"}, {"key": "value"}], "paging": {"next": "%s"}}' % next_url,
                      status=200,
                      content_type='application/json')

        responses.add(responses.GET, next_url,
                      body='{"data": [{"key": "value"}, {"key": "value"}, {"key": "value"}], "paging": {"next": ""}}',
                      status=200,
                      content_type='application/json')

        response = self.wrapper.test().get()

        iterations_count = 0
        for item in response().pages(max_pages=3):
            self.assertIn(item.key().data, 'value')
            iterations_count += 1

        self.assertEqual(iterations_count, 7)

    @responses.activate
    def test_simple_pages_max_page_zero_iterator(self):
        next_url = 'http://api.teste.com/next_batch'

        responses.add(responses.GET, self.wrapper.test().data,
                      body='{"data": [{"key": "value"}], "paging": {"next": "%s"}}' % next_url,
                      status=200,
                      content_type='application/json')

        responses.add(responses.GET, next_url,
                      body='{"data": [{"key": "value"}], "paging": {"next": ""}}',
                      status=200,
                      content_type='application/json')

        response = self.wrapper.test().get()

        iterations_count = 0
        for item in response().pages(max_pages=0):
            self.assertIn(item.key().data, 'value')
            iterations_count += 1

        self.assertEqual(iterations_count, 0)

    @responses.activate
    def test_simple_pages_max_item_zero_iterator(self):
        next_url = 'http://api.teste.com/next_batch'

        responses.add(responses.GET, self.wrapper.test().data,
                      body='{"data": [{"key": "value"}], "paging": {"next": "%s"}}' % next_url,
                      status=200,
                      content_type='application/json')

        responses.add(responses.GET, next_url,
                      body='{"data": [{"key": "value"}], "paging": {"next": ""}}',
                      status=200,
                      content_type='application/json')

        response = self.wrapper.test().get()

        iterations_count = 0
        for item in response().pages(max_items=0):
            self.assertIn(item.key().data, 'value')
            iterations_count += 1

        self.assertEqual(iterations_count, 0)

    @responses.activate
    def test_simple_pages_max_item_zero_iterator(self):
        next_url = 'http://api.teste.com/next_batch'

        responses.add(responses.GET, self.wrapper.test().data,
                      body='{"data": [{"key": "value"}], "paging": {"next": "%s"}}' % next_url,
                      status=200,
                      content_type='application/json')

        responses.add(responses.GET, next_url,
                      body='{"data": [{"key": "value"}], "paging": {"next": ""}}',
                      status=200,
                      content_type='application/json')

        response = self.wrapper.test().get()

        iterations_count = 0
        for item in response().pages(max_items=0):
            self.assertIn(item.key().data, 'value')
            iterations_count += 1

    @responses.activate
    def test_data_serialization(self):
        wrapper = SerializerClient()

        responses.add(responses.POST, self.wrapper.test().data,
                      body='{}', status=200, content_type='application/json')

        string_date = '2014-11-13T14:53:18.694072+00:00'
        string_decimal = '1.45'

        data = {
            'date': arrow.get(string_date).datetime,
            'decimal': Decimal(string_decimal),
        }

        wrapper.test().post(data=data)

        request_body = responses.calls[0].request.body

        self.assertEqual(
            json.loads(request_body),
            {'date': string_date, 'decimal': string_decimal})

