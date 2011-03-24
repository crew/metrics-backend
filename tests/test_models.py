import mongoengine
import unittest
from crew.flamongo.models import Namespace, ApiKey


class TestApiKey(unittest.TestCase):

    def setUp(self):
        mongoengine.connect('test')
        Namespace.drop_collection()
        ApiKey.drop_collection()

    def test_has_read(self):
        a = ApiKey()
        a.access = 'r'
        self.assertTrue(a.has_read)
        a.access = 'w'
        self.assertFalse(a.has_read)

    def test_has_write(self):
        a = ApiKey()
        a.access = 'w'
        self.assertTrue(a.has_write)
        a.access = 'r'
        self.assertFalse(a.has_write)

    def test_create(self):
        ns = Namespace(name='test', database='test')
        ns.save()
        # Create default, read-only.
        a = ApiKey.create(ns)
        self.assertTrue(a.has_read)
        self.assertFalse(a.has_write)
        # Create a read-writable.
        a = ApiKey.create(ns, 'rw')
        self.assertTrue(a.has_read)
        self.assertTrue(a.has_write)

    def test_find(self):
        ns = Namespace(name='test', database='test')
        ns.save()
        # negative case.
        a = ApiKey.find('test', 'blah')
        self.assertTrue(a is None)
        # positive case.
        a = ApiKey.create(ns)
        a.save()
        key = str(a)
        self.assertTrue(ApiKey.find('test', key) is not None)

    def test_repr(self):
        apikey = ApiKey(value='blah')
        x = eval(repr(apikey))


class TestNamespace(unittest.TestCase):

    def setUp(self):
        mongoengine.connect('test')

    def test_str(self):
        ns = Namespace(name='hello')
        self.assertEquals(str(ns), 'hello')

    def test_repr(self):
        ns = Namespace(name='hello', database='blah')
        # No crash
        x = eval(repr(ns))

    def test_apikeys(self):
        ns = Namespace(name='blah', database='blah')
        ns.save()
        apikeys = []
        for _ in range(10):
            a = ApiKey.create(ns)
            a.save()
            apikeys.append(a)
        self.assertEquals(len(ns.apikeys), 10)
        self.assertEquals(set(apikeys), set(ns.apikeys))

    def test_eq(self):
        ns = Namespace(name='hello', database='world')
        self.assertTrue(ns.__eq__(ns))
        # Only the name has to match.
        other = Namespace(name='hello', database='otherworld')
        self.assertTrue(ns.__eq__(other))

    def test_hash(self):
        ns = Namespace(name='hello')
        hash(ns)


if __name__ == '__main__':
    unittest.main()
