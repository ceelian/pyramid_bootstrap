import six


class BootstrapFactory(object):
    """
    Design:
     * Each bootstrap version has its own Bootstrap class.
     * Static assets of each bootstrap are prepared in build process.
    """

    bootstraps = []

    @classmethod
    def build(Cls, version, use_min_file=True, theme_name=None):
        assets = {
            'css': 'css/bootstrap.css',
            'theme': 'css/{}.css'.format(theme_name),
            'javascript': 'js/bootstrap.js',
        }
        if use_min_file:
            for key, value in six.iteritems(assets):
                assets[key] = value.replace(".", ".min.")
        assets['_prefix'] = 'pyramid_bootstrap:static/{}/'.format(version)

        class Bootstrap(object):

            TAGS = {
                'stylesheet': '<link rel="stylesheet" href="{}" />',
                'script': '<script src="{}"></script>'
            }

            def __init__(self, request):
                self.request = request

            def static_url(self, path):
                return self.request.static_url(self.assets['_prefix'] + path)

            @property
            def css_url(self):
                return self.static_url(self.assets['css'])

            @property
            def theme_url(self):
                return self.static_url(self.assets['theme'])

            @property
            def javascript_url(self):
                return self.static_url(self.assets['javascript'])

            @property
            def css(self):
                return self.TAGS['stylesheet'].format(self.css_url)

            @property
            def theme(self):
                return self.TAGS['stylesheet'].format(self.theme_url)

            @property
            def javascript(self):
                return self.TAGS['script'].format(self.javascript_url)

        Bootstrap.version = version
        Bootstrap.assets = assets
        return Bootstrap

    @classmethod
    def build_bootstraps(Cls, versions, use_min_file):
        Cls.versions = versions
        Cls.bootstraps = {
            ver: Cls.build(ver.strip(),
                           use_min_file=use_min_file)
            for ver in versions.split(",")
        }
        return Cls.bootstraps

    @classmethod
    def build_loader(Cls, request):
        if not Cls.bootstraps:
            raise Exception(("{cls}.bootstraps not built. See {cls}."
                             "build_bootstraps").format(cls=Cls.__name__))

        def load_bootstrap(version=None):
            if version is None:
                return six.itervalues(Cls.bootstraps).next()(request)
            else:
                try:
                    return Cls.bootstraps[version](request)
                except KeyError:
                    raise KeyError(
                        'Bootstrap version {} not found'.format(version))
        return load_bootstrap
