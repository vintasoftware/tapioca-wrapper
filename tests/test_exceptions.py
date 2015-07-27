# coding: utf-8

from __future__ import unicode_literals

import unittest

import responses
import requests

from tapioca.exceptions import (
    RequestError, ServerError, ResponseProcessException)

from tests.client import TestTapiocaClient, TestClientAdapter


class TestExceptions(unittest.TestCase):

    def setUp(self):
        self.wrapper = TestTapiocaClient()

    # @responses.activate
    # def test_adapter_raises_response_process_exception_on_400s(self):
    #     responses.add(responses.GET, self.wrapper.test().data(),
    #         body='{"erros": "Bad Request Error"}',
    #         status=400,
    #         content_type='application/json')

    #     with self.assertRaises(ResponseProcessException):
    #         TestClientAdapter().process_response(response)

    # @responses.activate
    # def test_adapter_raises_response_process_exception_on_500s(self):
    #     responses.add(responses.GET, self.wrapper.test().data(),
    #         body='{"erros": "Server Error"}',
    #         status=500,
    #         content_type='application/json')

    #     with self.assertRaises(ResponseProcessException):
    #         TestClientAdapter().process_response(response)

    @responses.activate
    def test_raises_request_error(self):
        responses.add(responses.GET, self.wrapper.test().data(),
            body='{"data": {"key": "value"}}',
            status=400,
            content_type='application/json')

        with self.assertRaises(RequestError):
            self.wrapper.test().get()

    @responses.activate
    def test_raises_server_error(self):
        responses.add(responses.GET, self.wrapper.test().data(),
            status=500,
            content_type='application/json')

        with self.assertRaises(ServerError):
            self.wrapper.test().get()

