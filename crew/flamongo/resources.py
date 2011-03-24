import json
import time
from models import ApiKey, Namespace
from twisted.web.resource import Resource
from twisted.python import log
from pymongo.database import Database
from pymongo.collection import Collection


class JSONResource(Resource):
    isLeaf = True

    def render(self, request):
        start = time.time()
        try:
            return Resource.render(self, request)
        except Exception, e:
            log.err(e)
            request.content.reset()
            log.err('Error: input: %s' % request.content.read())
        finally:
            end = time.time()
            log.msg('Time: %s ms' % ((end - start) * 1000))

    def render_POST(self, request):
        log.msg('Request: %s' % request)
        data = json.load(request.content)
        log.msg('Content: %s' % data)
        return self._handle(data, request)

    def _handle(self, data, request):
        raise NotImplementedError()


class MongoResource(JSONResource):

    def __init__(self, conn):
        self.conn = conn
        JSONResource.__init__(self)

    @staticmethod
    def datetime_to_float(dt):
        """
        Translate a datetime (UTC) into UNIX time.

        :param dt: A datetime object.
        >>> datetime_to_float(datetime(2010, 11, 2, 20, 38, 55, 123456))
        1288744735.123456
        >>> datetime_to_float(datetime(2010, 11, 2, 20, 38, 55, 1))
        1288744735.000001
        """
        return time.mktime(dt.timetuple()) + dt.microsecond / 1000000.0

    @classmethod
    def filter_results(cls, results):
        """
        Filters the results. Removes the _id field and converts the timestamp
        into UNIX time.

        :param results: The list of dicts returned from Mongo.
        """
        for x in results:
            del x['_id']
            if x.has_key('timestamp'):
                x['timestamp'] = cls.datetime_to_float(x['timestamp'])
            yield x

    @classmethod
    def db_name(cls, namespace):
        # FIXME
        # ns = Namespace.objects.get(name=namespace)
        # return ns.database
        return 'test'

    @classmethod
    def split_data(cls, data):
        data = dict(data)
        try:
            apikey = data['apikey']
            namespace = data['namespace']
            del data['apikey']
            del data['namespace']
        except KeyError:
            log.err('Malformed request %s' % data)
            raise
        return apikey, namespace, data

    @classmethod
    def has_read_access(cls, namespace, apikey):
        return True

    @classmethod
    def has_write_access(cls, namespace, apikey):
        a = ApiKey.find(namespace, apikey)
        if a:
            return a.has_write

    def get_collection(self, namespace):
        db = Database(self.conn, self.db_name(namespace))
        return Collection(db, namespace)
