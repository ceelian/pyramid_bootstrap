#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pyramid_bootstrap
----------------------------------

Tests for `pyramid_bootstrap` module.
"""

import unittest

from pyramid.config import Configurator

import pyramid_bootstrap


class TestPyramid_bootstrap(unittest.TestCase):

    def setUp(self):
        self.config = Configurator()

    def test_includeme(self):
        pyramid_bootstrap.includeme(self.config)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
