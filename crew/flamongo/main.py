from twisted.web import server
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.python import log
from store import StoreResource
from retrieve import RetrieveResource


class TopLevel(Resource):
    """The top-level web resource. Handles '/'"""

    def getChild(self, path, request):
        """Delegates the path to the correct resource."""
        if path == 'store':
            return StoreResource()
        elif path == 'retrieve':
            return RetrieveResource()


if __name__ == '__main__':
    import sys
    log.startLogging(sys.stderr)
    site = server.Site(TopLevel())
    reactor.listenTCP(2000, site)
    try:
        from twisted.internet import ssl
        ssl_context = ssl.DefaultOpenSSLContextFactory('test.key', 'test.crt')
        reactor.listenSSL(2443, site, ssl_context)
    except:
        log.msg('SSL not enabled. Needs PyOpenSSL.')
    reactor.run()
