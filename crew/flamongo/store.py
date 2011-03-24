import json
import uuid
import pymongo
from twisted.python import log
from resources import MongoResource
from datetime import datetime


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
        if not self.has_write_access(namespace, apikey):
            # XXX
            return '{"code":403,"error":"Unauthorized."}'
        coll = self.get_collection(namespace)
        if not coll.ensure_index('timestamp'):
            coll.create_index('timestamp', pymongo.ASCENDING)
        try:
            # XXX More data validation?
            data['timestamp'] = datetime.utcfromtimestamp(data['timestamp'])
            oid = coll.insert(data, safe=True)
            log.msg('Created: %s' % oid)
            return '{"code":201}'
        except Exception, e:
            error_id = uuid.uuid4()
            log.err('%s Error: %s' % (error_id, e))
            return '{"code":503,"error":"%s : Service Error"}' % error_id
        finally:
            self.conn.end_request()
