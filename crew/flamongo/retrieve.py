from twisted.python import log
from twisted.internet import defer
import json
import uuid
from resources import MongoResource
from pymongo.objectid import ObjectId
from pymongo.cursor import Cursor
import time
from datetime import datetime


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


def filter_results(results):
    """
    Filters the results. Removes the _id field and converts the timestamp
    into UNIX time.

    :param results: The list of dicts returned from Mongo.
    """
    for x in results:
        del x['_id']
        x['timestamp'] = datetime_to_float(x['timestamp'])
        yield x


class RetrieveResource(MongoResource):

    @classmethod
    def get_filter_and_fields(cls, data):
        fields = None
        if data.has_key('fields'):
            fields = data['fields']
            if 'timestamp' not in fields:
                fields.append('timestamp')
            # Check that 'timestamp' is not the only field
            if len(fields) == 1 and 'timestamp' in fields:
                fields = None
        q_filter = {}
        for k, v in data.iteritems():
            if isinstance(v, basestring):
                q_filter[k] = v
        # Add the start and end datetimes. $lt -> "<" and $gte -> ">="
        # start_time <= [...] < end_time
        q_filter['timestamp'] = {
            '$lt': datetime.utcfromtimestamp(data['end_time']),
            '$gte': datetime.utcfromtimestamp(data['start_time']),
        }
        return q_filter, fields

    @classmethod
    def validate(cls, data):
        assert data.has_key('start_time')
        assert data.has_key('end_time')
        assert type(data['start_time']) in [float, int]
        assert type(data['end_time']) in [float, int]

    def _handle(self, data, request):
        """
        :data: The deserialized JSON object.
        """
        if not self.conn:
            return '{"code":503,"error":"No database connection."}'
        try:
            apikey, namespace, data = self.split_data(data)
            self.validate(data)
        except:
            return '{"code":400,"error":"Bad request."}'
        # Parse the filters and the fields to fetch
        q_filter, fields = self.get_filter_and_fields(data)
        log.msg('Fields: %s' % str(fields))
        log.msg('Filters: %s' % str(q_filter))
        try:
            coll = self.get_collection(namespace)
            results = coll.find(q_filter, fields)
            return json.dumps(list(filter_results(results)),
                separators=(',', ':'))
        except Exception, e:
            error_id = uuid.uuid4()
            log.err('%s Error: %s' % (error_id, e))
            return '{"code":503,"error":"%s : Service Error"}' % error_id
        finally:
            self.conn.end_request()
