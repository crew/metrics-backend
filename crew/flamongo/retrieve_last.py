from twisted.python import log
import pymongo
import json
import uuid
from resources import MongoResource


class RetrieveLastResource(MongoResource):

    @classmethod
    def cleaned_data(cls, data):
        clean_data = {
            'limit': 1,
            'fields': None,
            'filters': {},
        }
        if data.has_key('limit'):
            assert 0 < data['limit'] <= 1000
            clean_data['limit'] = data['limit']
        if data.has_key('fields'):
            clean_data['fields'] = data['fields']
        if data.has_key('attributes'):
            attr = {}
            for k, v in data['attributes'].items():
                if isinstance(v, list):
                    attr[k] = {'$in': v}
                else:
                    attr[k] = v
            clean_data['filters'] = attr
        return clean_data

    def _handle(self, data, request):
        """
        :param data: The deserialized JSON object.
        :param request: The request object.
        :returns: result to the request.
        """
        if not self.conn:
            return '{"code":503,"error":"No database connection."}'
        try:
            apikey, namespace, data = self.split_data(data)
            log.msg(data)
            data = self.cleaned_data(data)
            log.msg(data)
        except:
            return '{"code":400,"error":"Bad request."}'
        fields = data['fields']
        filters = data['filters']
        limit = data['limit']
        log.msg('Fields: %s' % fields)
        log.msg('Filters: %s' % filters)
        try:
            coll = self.get_collection(namespace)
            results = coll.find(filters, fields).sort(
                'timestamp', pymongo.DESCENDING).limit(limit)
            return json.dumps(list(self.filter_results(results)),
                separators=(',', ':'))
        except Exception as e:
            log.err('Error: %s' % e)
            return '{"code":503,"error":"Service Error"}'
        finally:
            self.conn.end_request()
