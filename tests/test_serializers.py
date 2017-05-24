# coding: utf-8

from __future__ import unicode_literals

import arrow
import unittest
import responses
import json
from decimal import Decimal

from tapioca.serializers import BaseSerializer, SimpleSerializer

from tests.client import TesterClient, SerializerClient


class TestSerlializer(unittest.TestCase):

    def setUp(self):
        self.wrapper = SerializerClient()

    def test_passing_serializer_on_instatiation(self):
        wrapper = TesterClient(serializer_class=SimpleSerializer)
        serializer = wrapper._api.serializer
        self.assertTrue(isinstance(serializer, BaseSerializer))

    @responses.activate
    def test_external_serializer_is_passed_along_clients(self):
        serializer_wrapper = TesterClient(serializer_class=SimpleSerializer)

        responses.add(responses.GET, serializer_wrapper.test().data,
                      body='{"date": "2014-11-13T14:53:18.694072+00:00"}',
                      status=200,
                      content_type='application/json')

        response = serializer_wrapper.test().get()

        self.assertTrue(response._api.serializer.__class__, SimpleSerializer)

    def test_serializer_client_adapter_has_serializer(self):
        serializer = self.wrapper._api.serializer
        self.assertTrue(isinstance(serializer, BaseSerializer))

    @responses.activate
    def test_executor_dir_returns_serializer_methods(self):
        responses.add(responses.GET, self.wrapper.test().data,
                      body='{"date": "2014-11-13T14:53:18.694072+00:00"}',
                      status=200,
                      content_type='application/json')

        response = self.wrapper.test().get()

        e_dir = dir(response())

        self.assertIn('to_datetime', e_dir)
        self.assertIn('to_decimal', e_dir)

    @responses.activate
    def test_request_with_data_serialization(self):
        responses.add(responses.POST, self.wrapper.test().data,
                      body='{}', status=200, content_type='application/json')

        string_date = '2014-11-13T14:53:18.694072+00:00'
        string_decimal = '1.45'

        data = {
            'date': arrow.get(string_date).datetime,
            'decimal': Decimal(string_decimal),
        }

        self.wrapper.test().post(data=data)

        request_body = responses.calls[0].request.body

        self.assertEqual(
            json.loads(request_body),
            {'date': string_date, 'decimal': string_decimal})


class TestDeserialization(unittest.TestCase):

    def setUp(self):
        self.wrapper = SerializerClient()

    @responses.activate
    def test_convert_to_decimal(self):
        responses.add(responses.GET, self.wrapper.test().data,
                      body='{"decimal_value": "10.51"}',
                      status=200,
                      content_type='application/json')

        response = self.wrapper.test().get()
        self.assertEqual(
            response.decimal_value().to_decimal(),
            Decimal('10.51'))

    @responses.activate
    def test_convert_to_datetime(self):
        responses.add(responses.GET, self.wrapper.test().data,
                      body='{"date": "2014-11-13T14:53:18.694072+00:00"}',
                      status=200,
                      content_type='application/json')

        response = self.wrapper.test().get()
        date = response.date().to_datetime()
        self.assertEqual(date.year, 2014)
        self.assertEqual(date.month, 11)
        self.assertEqual(date.day, 13)
        self.assertEqual(date.hour, 14)
        self.assertEqual(date.minute, 53)
        self.assertEqual(date.second, 18)

    @responses.activate
    def test_call_non_existent_conversion(self):
        responses.add(responses.GET, self.wrapper.test().data,
                      body='{"any_data": "%#ˆ$&"}',
                      status=200,
                      content_type='application/json')

        response = self.wrapper.test().get()
        with self.assertRaises(NotImplementedError):
            response.any_data().to_blablabla()

    @responses.activate
    def test_call_conversion_with_no_serializer(self):
        wrapper = TesterClient()
        responses.add(responses.GET, wrapper.test().data,
                      body='{"any_data": "%#ˆ$&"}',
                      status=200,
                      content_type='application/json')

        response = wrapper.test().get()
        with self.assertRaises(NotImplementedError):
            response.any_data().to_datetime()

    @responses.activate
    def test_pass_kwargs(self):
        responses.add(responses.GET, self.wrapper.test().data,
                      body='{"decimal_value": "10.51"}',
                      status=200,
                      content_type='application/json')

        response = self.wrapper.test().get()

        self.assertEqual(
            response.decimal_value().to_kwargs(some_key='some value'),
            {'some_key': 'some value'})


class TestSerialization(unittest.TestCase):

    def setUp(self):
        self.serializer = SimpleSerializer()

    def test_serialize_int(self):
        data = 1

        serialized = self.serializer.serialize(data)

        self.assertEqual(serialized, data)

    def test_serialize_str(self):
        data = 'the str'

        serialized = self.serializer.serialize(data)

        self.assertEqual(serialized, data)

    def test_serialize_float(self):
        data = 1.23

        serialized = self.serializer.serialize(data)

        self.assertEqual(serialized, data)

    def test_serialize_none(self):
        data = None

        serialized = self.serializer.serialize(data)

        self.assertEqual(serialized, data)

    def test_serialization_of_simple_dict(self):
        data = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': 'value3',
        }

        serialized = self.serializer.serialize(data)

        self.assertEqual(serialized, data)

    def test_serialization_of_simple_list(self):
        data = [1, 2, 3, 4, 5]

        serialized = self.serializer.serialize(data)

        self.assertEqual(serialized, data)

    def test_serialization_of_nested_list_in_dict(self):
        data = {
            'key1': [1, 2, 3, 4, 5],
            'key2': [1],
            'key3': [1, 2, 5],
        }

        serialized = self.serializer.serialize(data)

        self.assertEqual(serialized, data)

    def test_multi_level_serializations(self):
        data = [
            {'key1': [1, 2, 3, 4, 5]},
            {'key2': [1]},
            {'key3': [1, 2, 5]},
        ]

        serialized = self.serializer.serialize(data)

        self.assertEqual(serialized, data)

    def test_decimal_serialization(self):
        data = {
            'key': [Decimal('1.0'), Decimal('1.1'), Decimal('1.2')]
        }

        serialized = self.serializer.serialize(data)

        self.assertEqual(serialized, {'key': ['1.0', '1.1', '1.2']})

    def test_datetime_serialization(self):
        string_date = '2014-11-13T14:53:18.694072+00:00'

        data = [arrow.get(string_date).datetime]

        serialized = self.serializer.serialize(data)

        self.assertEqual(serialized, [string_date])
