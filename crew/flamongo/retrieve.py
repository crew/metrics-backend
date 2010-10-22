from twisted.web.resource import Resource
import json


class RetrieveResource(Resource):
    isLeaf = True

    def render_POST(self, request):
        # TODO implement this!
        return json.dumps({'not': 'implemented'})
