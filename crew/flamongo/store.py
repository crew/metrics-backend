from twisted.python import log
import json
from resources import MongoResource
import pymongo
import uuid


class StoreResource(MongoResource):

    def _handle(self, data, request):
        """
        :data: The deserialized JSON object.
        """
        if not self.conn:
            return '{"code":503,"error":"No database connection."}'
        try:
            apikey, namespace, data = self.split_data(data)
        except:
            return '{"code":400,"error":"Bad request."}'
        coll = self.get_collection(namespace)
        if not coll.ensure_index('timestamp'):
            coll.create_index('timestamp', pymongo.ASCENDING)
        try:
            oid = coll.insert(data)
            log.msg('Created: %s' % oid)
            return '{"code":201}'
        except Exception, e:
            error_id = uuid.uuid4()
            log.err('%s Error: %s' % (error_id, e))
            return '{"code":503,"error":"%s : Service Error"}' % error_id
        finally:
            self.conn.end_request()
