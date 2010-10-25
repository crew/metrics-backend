from twisted.web.resource import Resource
from twisted.python import log
from pymongo.database import Database
from pymongo.collection import Collection
import json
import time


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

    @classmethod
    def db_name(cls, namespace):
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

    def get_collection(self, namespace):
        db = Database(self.conn, self.db_name(namespace))
        return Collection(db, namespace)
