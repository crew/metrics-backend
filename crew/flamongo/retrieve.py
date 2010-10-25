from twisted.python import log
from twisted.internet import defer
import json
import uuid
from resources import MongoResource
from pymongo.objectid import ObjectId
from pymongo.cursor import Cursor
from bson.son import SON


class RetrieveResource(MongoResource):

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
        q_filter = {}
        fields = None
        for k, v in data.iteritems():
            if k == 'fields' and v:
                fields = v
                if 'timestamp' not in v:
                    fields.append('timestamp')
            elif isinstance(v, basestring):
                q_filter[k] = v
        log.msg('Fields: %s' % str(fields))
        log.msg('Filters: %s' % str(q_filter))
        try:
            coll = self.get_collection(namespace)
            acc = []
            for y in coll.find(q_filter, fields):
                del y['_id']
                acc.append(y)
            return json.dumps(acc, separators=(',', ':'))
        except Exception, e:
            error_id = uuid.uuid4()
            log.err('%s Error: %s' % (error_id, e))
            return '{"code":503,"error":"%s : Service Error"}' % error_id
        finally:
            self.conn.end_request()
