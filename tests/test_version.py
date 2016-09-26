#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of smart-sentinel.
# https://github.com/rfloriano/smart-sentinel

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2016, Rafael Floriano da Silva <rflorianobr@gmail.com>

from preggy import expect

from smart_sentinel import __version__
from tests.base import TestCase


class VersionTestCase(TestCase):
    def test_has_proper_version(self):
        expect(__version__).to_equal('0.1.0')
