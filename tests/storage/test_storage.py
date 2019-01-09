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
        storage._storage[1] = ('test',)
        storage._temp[2] = {1: ('updated',)}
        response = storage.get_row(1, 'main', 1, 1)
        self.assertEqual(response, {1: {'value': 'test'}})

    def test_prefers_transaction_specific_value(self):
        storage._storage[1] = ('test'),
        storage._temp[2] = {1: ('updated',)}
        response = storage.get_row(2, 'main', 1, 1)
        self.assertEqual(response, {1: {'value': 'updated'}})

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
        storage._storage[1] = ('test',)
        storage._temp[2] = dict()
        response = storage.write_row(2, 'main', 1, {'value': 'updated'}, 1)
        self.assertEqual(storage._temp[2][1], ('updated',))
        self.assertEqual(storage._storage[1], ('test',))

    def tearDown(self):
        storage._storage = dict()
        storage._temp = dict()
