import six


class BootstrapFactory(object):
    """
    Design:
     * Each bootstrap version has its own Bootstrap class.
     * Static assets of each bootstrap are prepared in build process.
    """

    bootstraps = []
    TAGS = {
        'stylesheet': '<link rel="stylesheet" href="{}" />',
        'script': '<script src="{}"></script>'
    }

    @classmethod
    def build(Cls, version, use_min_file=True, theme_name='bootstrap-theme'):
        assets = {
            'css': 'css/bootstrap.css',
            'theme': 'css/{}.css'.format(theme_name),
            'javascript': 'js/bootstrap.js',
        }
        if use_min_file:
            for key, value in six.iteritems(assets):
                assets[key] = value.replace(".", ".min.")
        assets['_prefix'] = 'pyramid_bootstrap:static/{}/'.format(version)

        def build_css_property(cls, name):

            css_url = name + "_url"
            css_url_not_min = css_url + "_not_min"

            def url(self):
                return self.static_url(self.assets[name])

            def url_not_min(self):
                return self.static_url_not_min(self.assets[name])

            def tag(self):
                return Cls.TAGS['stylesheet'].format(getattr(self, css_url))

            def tag_not_min(self):
                return Cls.TAGS['stylesheet'].format(getattr(self,
                                                             css_url_not_min))
            setattr(cls, css_url, property(url))
            setattr(cls, css_url_not_min, property(url_not_min))
            setattr(cls, name, property(tag))
            setattr(cls, name + '_not_min', property(tag_not_min))

        def build_js_property(cls, name):

            js_url = name + "_url"
            js_url_not_min = js_url + '_not_min'

            def url(self):
                return self.static_url(self.assets[name])

            def url_not_min(self):
                return self.static_url_not_min(self.assets[name])

            def tag(self):
                return Cls.TAGS['script'].format(getattr(self, js_url))

            def tag_not_min(self):
                return Cls.TAGS['script'].format(getattr(self, js_url_not_min))
            setattr(cls, js_url, property(url))
            setattr(cls, js_url_not_min, property(url_not_min))
            setattr(cls, name, property(tag))
            setattr(cls, name + '_not_min', property(tag_not_min))

        class Bootstrap(object):

            def __init__(self, request):
                self.request = request

            def static_url(self, path):
                return self.request.static_url(self.assets['_prefix'] + path)

            def static_url_not_min(self, path):
                return self.static_url(path.replace(".min.", "."))

        Bootstrap.version = version
        Bootstrap.assets = assets
        for name in ('css', 'theme'):
            build_css_property(Bootstrap, name)
        build_js_property(Bootstrap, 'javascript')
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
