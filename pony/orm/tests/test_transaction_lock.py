import unittest


from pony.orm import *
from pony.orm.tests import setup_database, teardown_database

db = Database()


class MockPost(db.Entity):
    category = Optional('MockCategory')
    name = Optional(str, default='Noname')


class MockCategory(db.Entity):
    posts = Set(MockPost)


class TransactionLockTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        setup_database(db)
        with db_session:
            cls.post = MockPost(id=1)

    @classmethod
    def tearDownClass(cls):
        teardown_database(db)

    __call__ = db_session(unittest.TestCase.__call__)

    def tearDown(self):
        rollback()

    def test_create(self):
        p = MockPost(id=2)
        p.flush()
        cache = db._get_cache()
        self.assertEqual(cache.immediate, True)
        self.assertEqual(cache.in_transaction, True)

    def test_update(self):
        p = MockPost[self.post.id]
        p.name = 'Trash'
        p.flush()
        cache = db._get_cache()
        self.assertEqual(cache.immediate, True)
        self.assertEqual(cache.in_transaction, True)

    def test_delete(self):
        p = MockPost[self.post.id]
        p.delete()
        flush()
        cache = db._get_cache()
        self.assertEqual(cache.immediate, True)
        self.assertEqual(cache.in_transaction, True)
