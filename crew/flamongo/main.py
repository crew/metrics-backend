import sys
import tempfile
from twisted.web import server
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.python import log
from store import StoreResource
from retrieve import RetrieveResource
from retrieve_last import RetrieveLastResource
from pymongo.connection import Connection
import utils
import gflags


FLAGS = gflags.FLAGS
gflags.DEFINE_integer('port', 2000, 'The port number')
gflags.DEFINE_integer('secureport', 2443, 'The secure port number')
gflags.DEFINE_string('privatekey', 'test.key', 'The location of the private '
    'key for SSL')
gflags.DEFINE_string('certificate', 'test.crt', 'The location of the SSL '
    'certificate.')
gflags.DEFINE_string('logfile', None, 'The filename of the log.')
gflags.DEFINE_boolean('daemonize', False, 'Daemonize.')


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
        elif path == 'retrieve-last':
            return RetrieveLastResource(self.get_conn())


def main(argv):
    FLAGS(argv)
    if not FLAGS.logfile and not FLAGS.daemonize:
        # No log file and not daemonized.
        log.startLogging(sys.stderr)
    elif not FLAGS.logfile and FLAGS.daemonize:
        # Daemonized, but no log file.
        fd, name = tempfile.mkstemp(prefix='flamongo', suffix='.log')
        os.close(fd)
        sys.stderr.write('Logging to %s\n' % name)
        log.startLogging(open(name, 'a'))
    else:
        f = open(FLAGS.logfile, 'a')
        log.startLogging(f)
    # TODO define connection options.
    site = server.Site(TopLevel(lambda: Connection()))
    reactor.listenTCP(FLAGS.port, site)
    try:
        from twisted.internet import ssl
        ssl_context = ssl.DefaultOpenSSLContextFactory(FLAGS.privatekey,
            FLAGS.certificate)
        reactor.listenSSL(FLAGS.secureport, site, ssl_context)
    except ImportError:
        # removes the partial import.
        ssl = None
        log.err('SSL not enabled. Needs PyOpenSSL.')
    except Exception as ex:
        log.err(str(ex))
    if FLAGS.daemonize:
        utils.daemonize()
    reactor.run()


if __name__ == '__main__':
    main(sys.argv)
