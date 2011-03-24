import uuid
import mongoengine
from mongoengine import Document, StringField, ListField, ReferenceField


class ApiKey(Document):
    """
    :param namespace: The Namespace (reference).
    :param value: The value of the key (unique). This should be kept
        secret.
    :param access: The access information. Right now this is represented
        as a string. An 'r' in the string gives you read access. A 'w'
        gives you write access.
    """
    namespace = ReferenceField('Namespace', required=True)
    value = StringField(max_length=64, primary_key=True, required=True)
    access = StringField(max_length=20, required=True, default='r')

    @classmethod
    def create(cls, namespace, access='r'):
        """
        :param namespace: The namespace (reference).
        :param access: The access. One of ('r', 'rw', 'w').
        :returns: An ApiKey (unsaved).
        :rtype: :class:`ApiKey`.
        """
        return cls(value=str(uuid.uuid4()), access=access,
            namespace=namespace)

    @classmethod
    def find(cls, namespace, value):
        """
        :param str namespace: The namespace.
        :param str value: The apikey.
        :returns: The apikey in the given namespace, if found. Otherwise,
            None.
        """
        try:
            a = cls.objects.get(value=value)
        except (cls.DoesNotExist, cls.MultipleObjectsReturned):
            return
        if a.namespace.name == namespace:
            return a

    @property
    def has_read(self):
        """
        :returns: True if this ApiKey has read access.
        """
        return 'r' in self.access

    @property
    def has_write(self):
        """
        :returns: True if this ApiKey has write access.
        """
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
    """
    :param name: The name of this namespace.
    :param database: The name of the database.
    """
    name = StringField(max_length=50, required=True, primary_key=True)
    database = StringField(max_length=50, required=True,
        validation=lambda x: x != 'flamongo')
    # TODO schema validation

    @property
    def apikeys(self):
        """
        :returns: The list of ApiKeys associated with this namespace.
        """
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
