from twisted.python import log
import json
from resources import JSONResource


class StoreResource(JSONResource):

    def _handle(self, data):
        """
        :data: The deserialized JSON object.
        """
        # TODO implement this!
        return json.dumps({'not': 'implemented'})
