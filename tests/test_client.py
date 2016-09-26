#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of smart-sentinel.
# https://github.com/rfloriano/smart-sentinel

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2016, Rafael Floriano da Silva <rflorianobr@gmail.com>
import uuid
import mock

import redis
from preggy import expect

from smart_sentinel.client import SmartSentinel
from tests.base import TestCase


class ClientTestCase(TestCase):
    def test_should_execute_simple_operations(self):
        value = str(uuid.uuid4())
        self.client.set('testing', value)
        expect(self.client.get('testing')).to_equal(value)

    def test_should_compatible_with_items_interface(self):
        value = str(uuid.uuid4())
        self.client['testing'] = value
        expect(self.client['testing']).to_equal(value)
        del self.client['testing']

    def test_should_list_redis_methods(self):
        props = dir(self.client)
        # zremrangebylex not implemented by us,
        # should return redis client zremrangebylex method
        expect(props).to_include('zremrangebylex')

    @mock.patch('smart_sentinel.client.SmartSentinel._get_master')
    @mock.patch('redis.client.StrictRedis.set')
    def test_should_reselect_master_if_operation_fail(self, mocked_set, mocked_get_master):
        mocked_set.__name__ = 'set'
        mocked_set.side_effect = redis.exceptions.ConnectionError(
            'some conn error'
        )
        mocked_get_master().set = mock.Mock()
        value = str(uuid.uuid4())
        self.client.set('testing', value)
        mocked_get_master.assert_any_call()
        mocked_get_master().set.assert_called_once()

    @mock.patch('smart_sentinel.client.SmartSentinel._get_slave')
    @mock.patch('redis.client.StrictRedis.get')
    def test_should_reselect_slave_if_operation_fail(self, mocked_get, mocked_get_slave):
        mocked_get.__name__ = 'get'
        mocked_get.side_effect = redis.exceptions.ConnectionError(
            'some conn error'
        )
        mocked_get_slave().get = mock.Mock()
        value = str(uuid.uuid4())
        self.client.get('testing', value)
        mocked_get_slave.assert_any_call()
        mocked_get_slave().get.assert_called_once()
