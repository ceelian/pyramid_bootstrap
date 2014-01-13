from pyramid.events import subscriber
from pyramid.events import BeforeRender
from . import BootstrapFactory


@subscriber(BeforeRender)
def add_bootstrap_renderer(event):
    event['load_bootstrap'] = BootstrapFactory.build_loader(event['request'])
