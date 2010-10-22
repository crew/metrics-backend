from twisted.web.resource import Resource
from twisted.python import log
import json


class JSONResource(Resource):
    isLeaf = True

    def render(self, request):
        try:
            return Resource.render(self, request)
        except Exception, e:
            log.msg(e)
            request.content.reset()
            log.msg('Error: input: %s' % request.content.read())

    def render_POST(self, request):
        log.msg('Request: %s' % request)
        data = json.load(request.content)
        log.msg('Content: %s' % data)
        return self._handle(data)

    def _handle(self, data):
        raise NotImplementedError()
