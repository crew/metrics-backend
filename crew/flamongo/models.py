import uuid
import mongoengine
from mongoengine import Document, StringField, ListField, ReferenceField


class ApiKey(Document):
    namespace = ReferenceField('Namespace', required=True)
    value = StringField(max_length=64, primary_key=True, required=True)
    access = StringField(max_length=20, required=True, default='r')

    @classmethod
    def create(cls, namespace, access='r'):
        return cls(value=str(uuid.uuid4()), access=access,
            namespace=namespace)

    @classmethod
    def find(cls, namespace, value):
        try:
            a = cls.objects.get(value=value)
        except (cls.DoesNotExist, cls.MultipleObjectsReturned):
            return
        if a.namespace.name == namespace:
            return a

    @property
    def has_read(self):
        return 'r' in self.access

    @property
    def has_write(self):
        return 'w' in self.access

    def __repr__(self):
        return '%s(namespace=%r, value=%r, access=%r)' % (
            self.__class__.__name__, self.namespace, self.value,
            self.access)

    def __str__(self):
        return self.value

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.value == other.value


class Namespace(Document):
    name = StringField(max_length=50, required=True, primary_key=True)
    database = StringField(max_length=50, required=True,
        validation=lambda x: x != 'flamongo')
    # TODO schema validation

    @property
    def apikeys(self):
        return ApiKey.objects(namespace=self)

    def __repr__(self):
        return '%s(name=%r, database=%r)' % (self.__class__.__name__,
            self.name, self.database)

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name
