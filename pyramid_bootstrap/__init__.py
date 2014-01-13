#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Keith Yang'
__email__ = 'yang@keitheis.org'
__version__ = '0.1.0'


from pyramid.settings import asbool

from .bootstrap import BootstrapFactory


def includeme(config):
    DEFAULT = {
        'versions': '3.0.3',
        'use_min_file': True,
        'use_cdn': False,
        'static_path': {
            'cdn': "//netdna.bootstrapcdn.com/bootstrap/",
            'local': 'bootstrap/'
        },
        'cache_max_age': 3600,
    }

    settings = config.get_settings()
    setting_prefix = "bootstrap."

    def get_setting(attr, default=None):
        return settings.get(setting_prefix + attr, default)

    versions = get_setting('versions', DEFAULT['versions'])
    use_min_file = asbool(get_setting("use_min_file", DEFAULT['use_min_file']))
    bootstraps = BootstrapFactory.build_bootstraps(versions, use_min_file)

    use_cdn = asbool(get_setting("use_cdn"))
    if use_cdn:
        static_path = DEFAULT['static_path']['cdn']
    else:
        static_path = get_setting('static_path',
                                  DEFAULT['static_path']['local'])

    cache_max_age = get_setting('cache_max_age', DEFAULT['cache_max_age'])
    for version in bootstraps:
        config.add_static_view(static_path + version,
                               "pyramid_bootstrap:static/{}".format(version),
                               cache_max_age=cache_max_age)
    config.scan('pyramid_bootstrap.event_subscribers')
