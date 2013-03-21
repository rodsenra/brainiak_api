import json
from unittest import TestCase
from tornado.testing import AsyncTestCase, AsyncHTTPTestCase
from brainiak import server, greenlet_tornado


class TornadoAsyncTestCase(AsyncTestCase):

    def setUp(self):
        super(TornadoAsyncTestCase, self).setUp()
        greenlet_tornado.greenlet_set_ioloop(self.io_loop)

    # Disabling timeout for debugging purposes
    def wait(self, condition=None, timeout=None):
        return super(TornadoAsyncTestCase, self).wait(condition, timeout)


class TornadoAsyncHTTPTestCase(AsyncHTTPTestCase):

    def setUp(self):
        super(TornadoAsyncHTTPTestCase, self).setUp()
        greenlet_tornado.greenlet_set_ioloop(self.io_loop)

    def get_app(self):
        return server.Application()

    # Disabling timeout for debugging purposes
    def wait(self, condition=None, timeout=None):
        return super(TornadoAsyncHTTPTestCase, self).wait(condition, timeout)


class MockRequest(object):
    headers = {'Host': 'localhost:5100'}

    def __init__(self, query_string="", instance=""):
        self.query = query_string
        self.uri = "http://%s/ctx/klass" % self.headers['Host']
        if instance:
            self.uri = "%s/%s" % (self.uri, instance)
        if query_string:
            self.uri = "%s?%s" % (self.uri, query_string)

    def full_url(self):
        return self.uri
