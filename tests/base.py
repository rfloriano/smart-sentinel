#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of smart-sentinel.
# https://github.com/rfloriano/smart-sentinel

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2016, Rafael Floriano da Silva <rflorianobr@gmail.com>

from unittest import TestCase as PythonTestCase

import tornado.web
from tornado.testing import AsyncHTTPTestCase

from smart_sentinel.client import SmartSentinel


class TestCase(PythonTestCase):
    def setUp(self, *args, **kwargs):
        super(TestCase, self).setUp(*args, **kwargs)
        self.args = self.get_client_args()
        self.kwargs = self.get_client_kwargs()
        self.master_name = self.get_master_name()
        self.client = self.get_client(
            self.master_name,
            *self.args,
            **self.kwargs
        )

    def get_client(self, *args, **kwargs):
        return SmartSentinel(*args, **kwargs)

    def get_master_name(self):
        return 'master2'

    def get_client_args(self):
        return ([('localhost', 57574), ('localhost', 57573)],)

    def get_client_kwargs(self):
        return {}


class TornadoTestCase(AsyncHTTPTestCase, TestCase):
    def get_handlers(self):
        return []

    def get_app(self):
        return tornado.web.Application(self.get_handlers())
