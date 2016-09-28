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
from tornado.testing import gen_test
from preggy import expect

from smart_sentinel.tornado_client import TornadoSmartSentinel, TornadoStrictRedis
from tests.base import TornadoTestCase


class TornadoStrictRedisTestCase(TornadoTestCase):
    def get_client(self, *args, **kwargs):
        return TornadoStrictRedis()

    @gen_test
    def test_should_execute_simple_operations(self):
        value = str(uuid.uuid4())
        yield self.client.set('testing', value)
        expected = yield self.client.get('testing')
        expect(expected).to_equal(value)

    def test_should_compatible_with_items_interface(self):
        value = str(uuid.uuid4())
        with expect.error_to_happen(NotImplementedError):
            self.client['testing'] = value

        with expect.error_to_happen(NotImplementedError):
            self.client['testing']

        with expect.error_to_happen(NotImplementedError):
            del self.client['testing']

    def test_should_list_redis_methods(self):
        props = dir(self.client)
        # zremrangebylex not implemented by us,
        # should return redis client zremrangebylex method
        expect(props).to_include('zremrangebylex')


class TornadoSmartSentinelTestCase(TornadoTestCase):
    def get_client(self, *args, **kwargs):
        return TornadoSmartSentinel(*args, **kwargs)

    @gen_test
    def test_should_execute_simple_operations(self):
        value = str(uuid.uuid4())
        yield self.client.set('testing', value)
        expected = yield self.client.get('testing')
        expect(expected).to_equal(value)

    def test_should_compatible_with_items_interface(self):
        value = str(uuid.uuid4())
        with expect.error_to_happen(NotImplementedError):
            self.client['testing'] = value

        with expect.error_to_happen(NotImplementedError):
            self.client['testing']

        with expect.error_to_happen(NotImplementedError):
            del self.client['testing']

    def test_should_list_redis_methods(self):
        props = dir(self.client)
        # zremrangebylex not implemented by us,
        # should return redis client zremrangebylex method
        expect(props).to_include('zremrangebylex')

    @gen_test
    def test_should_reselect_master_if_operation_fail(self):
        with mock.patch.object(self.client._master, 'set') as mocked_set:
            with mock.patch.object(self.client, '_get_master') as mocked_get_master:
                mocked_set.__name__ = 'set'
                mocked_set.side_effect = redis.exceptions.ConnectionError('some conn error')
                value = str(uuid.uuid4())
                yield self.client.set('testing', value)
                mocked_get_master.assert_any_call()
                mocked_get_master().set.assert_called_once()

    @gen_test
    def test_should_reselect_slave_if_operation_fail(self):
        with mock.patch.object(self.client._slave, 'get') as mocked_get:
            with mock.patch.object(self.client, '_get_slave') as mocked_get_slave:
                mocked_get.__name__ = 'get'
                mocked_get.side_effect = redis.exceptions.ConnectionError(
                    'some conn error'
                )
                yield self.client.get('testing')
                mocked_get_slave.assert_any_call()
                mocked_get_slave().get.assert_called_once()
