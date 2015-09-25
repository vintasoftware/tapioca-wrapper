# coding: utf-8

from __future__ import unicode_literals

import unittest
import responses
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

    def test_serializer_client_adapter_has_serializer(self):
        serializer = self.wrapper._api.serializer
        self.assertTrue(isinstance(serializer, BaseSerializer))

    @responses.activate
    def test_convert_to_decimal(self):
        responses.add(responses.GET, self.wrapper.test().data(),
                      body='{"decimal_value": "10.51"}',
                      status=200,
                      content_type='application/json')

        response = self.wrapper.test().get()
        self.assertEqual(response.decimal_value().to_decimal(),
            Decimal('10.51'))

    @responses.activate
    def test_convert_to_datetime(self):
        responses.add(responses.GET, self.wrapper.test().data(),
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
        responses.add(responses.GET, self.wrapper.test().data(),
                      body='{"any_data": "%#ˆ$&"}',
                      status=200,
                      content_type='application/json')

        response = self.wrapper.test().get()
        with self.assertRaises(NotImplementedError):
            response.any_data().to_blablabla()

    @responses.activate
    def test_call_conversion_with_no_serializer(self):
        wrapper = TesterClient()
        responses.add(responses.GET, wrapper.test().data(),
                      body='{"any_data": "%#ˆ$&"}',
                      status=200,
                      content_type='application/json')

        response = wrapper.test().get()
        with self.assertRaises(NotImplementedError):
            response.any_data().to_datetime()
