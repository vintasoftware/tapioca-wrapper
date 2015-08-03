# coding: utf-8

from __future__ import unicode_literals

import unittest

import responses
import requests

from tapioca.tapioca import TapiocaClient

from tests.client import TesterClient


class TestTapiocaClient(unittest.TestCase):

    def setUp(self):
        self.wrapper = TesterClient()

    def test_fill_url_template(self):
        expected_url = 'https://api.test.com/user/123/'

        resource = self.wrapper.user(id='123')

        self.assertEqual(resource.data(), expected_url)

    def test_calling_len_on_tapioca_list(self):
        client = self.wrapper._wrap_in_tapioca([0,1,2])
        self.assertEqual(len(client), 3)

    def test_iterated_client_items_should_be_tapioca_instances(self):
        client = self.wrapper._wrap_in_tapioca([0,1,2])

        for item in client:
            self.assertTrue(isinstance(item, TapiocaClient))

    def test_iterated_client_items_should_contain_list_items(self):
        client = self.wrapper._wrap_in_tapioca([0,1,2])

        for i, item in enumerate(client):
            self.assertEqual(item().data(), i)


class TestTapiocaExecutor(unittest.TestCase):

    def setUp(self):
        self.wrapper = TesterClient()

    def test_resource_executor_data_should_be_composed_url(self):
        expected_url = 'https://api.test.com/test/'
        resource = self.wrapper.test()

        self.assertEqual(resource.data(), expected_url)

    def test_docs(self):
        self.assertEqual('\n'.join(self.wrapper.resource.__doc__.split('\n')[1:]),
                          'Resource: ' + self.wrapper.resource._resource['resource'] + '\n'
                          'Docs: ' + self.wrapper.resource._resource['docs'] + '\n'
                          'Foo: ' + self.wrapper.resource._resource['foo'] + '\n'
                          'Spam: ' + self.wrapper.resource._resource['spam'])

    def test_is_possible_to_access_wrapped_data_attributes(self):
        client = self.wrapper._wrap_in_tapioca([0,1,2])
        client().reverse()
        self.assertEqual(client().data(), [2,1,0])

    def test_get_dictionary_items_through_executor(self):
        client = self.wrapper._wrap_in_tapioca({'test': 'test value'})
        print client().items()


class TestTapiocaExecutorRequests(unittest.TestCase):

    def setUp(self):
        self.wrapper = TesterClient()

    def test_when_executor_has_no_response(self):
        with self.assertRaisesRegexp(Exception, "has no response"):
            self.wrapper.test().response()

    @responses.activate
    def test_get_request(self):
        responses.add(responses.GET, self.wrapper.test().data(),
            body='{"data": {"key": "value"}}',
            status=200,
            content_type='application/json')

        response = self.wrapper.test().get()

        self.assertEqual(response().data(), {'data': {'key': 'value'}})

    @responses.activate
    def test_access_response_field(self):
        responses.add(responses.GET, self.wrapper.test().data(),
            body='{"data": {"key": "value"}}',
            status=200,
            content_type='application/json')

        response = self.wrapper.test().get()

        response_data = response.data()

        self.assertEqual(response_data.data(), {'key': 'value'})

    @responses.activate
    def test_post_request(self):
        responses.add(responses.POST, self.wrapper.test().data(),
            body='{"data": {"key": "value"}}',
            status=201,
            content_type='application/json')

        response = self.wrapper.test().post()

        self.assertEqual(response().data(), {'data': {'key': 'value'}})

    @responses.activate
    def test_put_request(self):
        responses.add(responses.PUT, self.wrapper.test().data(),
            body='{"data": {"key": "value"}}',
            status=201,
            content_type='application/json')

        response = self.wrapper.test().put()

        self.assertEqual(response().data(), {'data': {'key': 'value'}})

    @responses.activate
    def test_patch_request(self):
        responses.add(responses.PATCH, self.wrapper.test().data(),
            body='{"data": {"key": "value"}}',
            status=201,
            content_type='application/json')

        response = self.wrapper.test().patch()

        self.assertEqual(response().data(), {'data': {'key': 'value'}})

    @responses.activate
    def test_delete_request(self):
        responses.add(responses.DELETE, self.wrapper.test().data(),
            body='{"data": {"key": "value"}}',
            status=201,
            content_type='application/json')

        response = self.wrapper.test().delete()

        self.assertEqual(response().data(), {'data': {'key': 'value'}})

    @responses.activate
    def test_simple_pages_iterator(self):
        next_url = 'http://api.teste.com/next_batch'

        responses.add(responses.GET, self.wrapper.test().data(),
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
            self.assertIn(item.key().data(), 'value')
            iterations_count += 1

        self.assertEqual(iterations_count, 2)


if __name__ == '__main__':
    unittest.main()
