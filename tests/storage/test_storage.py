import unittest

from pokedb import storage


class TestReadRow(unittest.TestCase):

    def setUp(self):
        storage._storage = dict()
        storage._temp = dict()
        storage._temp[1] = dict()
        storage._temp[2] = dict()

    def test_returns_none_if_data_does_not_exist(self):
        response = storage.get_row(1, 'main', 1, 2)
        self.assertEqual(response, {1: None})

    def test_returns_stored_value(self):
        fmt = storage._table_schema.get('main')
        storage._storage[1] = storage.serializer.serialize(fmt, 'test')
        storage._temp[2] = {1: storage.serializer.serialize(fmt, 'updated')}
        response = storage.get_row(1, 'main', 1, 1)
        self.assertEqual(response, {1: ('test',)})

    def test_prefers_transaction_specific_value(self):
        fmt = storage._table_schema.get('main')
        storage._storage[1] = storage.serializer.serialize(fmt, 'test'),
        storage._temp[2] = {1: storage.serializer.serialize(fmt, 'updated')}
        response = storage.get_row(2, 'main', 1, 1)
        self.assertEqual(response, {1: ('updated',)})

    def tearDown(self):
        storage._storage = dict()
        storage._temp = dict()


class TestWriteRow(unittest.TestCase):

    def setUp(self):
        storage._storage = dict()
        storage._temp = dict()
        storage._temp[1] = dict()
        storage._temp[2] = dict()

    def test_does_not_write_over_main_table(self):
        fmt = storage._table_schema.get('main')
        storage._storage[1] = storage.serializer.serialize(fmt, 'test')
        storage._temp[2] = dict()
        response = storage.write_row(2, 'main', 1, ('updated',), 1)
        self.assertEqual(storage._temp[2][1], storage.serializer.serialize(fmt, 'updated'))
        self.assertEqual(storage._storage[1], storage.serializer.serialize(fmt, 'test'))

    def tearDown(self):
        storage._storage = dict()
        storage._temp = dict()
