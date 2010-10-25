from twisted.web import server
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.python import log
from store import StoreResource
from retrieve import RetrieveResource
from pymongo.connection import Connection


class TopLevel(Resource):
    """The top-level web resource. Handles '/'"""

    def __init__(self, conn_f):
        """
        :param conn_f: The connection function.
        """
        self.conn_f = conn_f
        self.__conn = None
        Resource.__init__(self)

    def get_conn(self):
        """
        :returns: The Mongo Connection object or None if unable to connect.
        """
        if self.__conn:
            return self.__conn
        try:
            self.__conn = self.conn_f()
            return self.__conn
        except:
            log.err('Unable to connect to database.')

    def getChild(self, path, request):
        """Delegates the path to the correct resource."""
        if path == 'store':
            return StoreResource(self.get_conn())
        elif path == 'retrieve':
            return RetrieveResource(self.get_conn())


if __name__ == '__main__':
    import sys
    log.startLogging(sys.stderr)
    site = server.Site(TopLevel(lambda: Connection()))
    reactor.listenTCP(2000, site)
    try:
        from twisted.internet import ssl
        ssl_context = ssl.DefaultOpenSSLContextFactory('test.key', 'test.crt')
        reactor.listenSSL(2443, site, ssl_context)
    except:
        log.err('SSL not enabled. Needs PyOpenSSL.')
    reactor.run()
