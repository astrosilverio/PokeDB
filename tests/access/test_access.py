import unittest
from mock import patch

from pokedb import access, locks, storage
from pokedb.locks.exceptions import LockException


class TestAccessStartUp(unittest.TestCase):

    def test_btree_loads_on_startup(self):
        pass


class TestReadRow(unittest.TestCase):

    def setUp(self):
        storage._storage = dict()
        storage._temp = dict()
        storage._temp[1] = dict()
        storage._temp[2] = dict()

        locks.start()

    def test_calls_lock_module_to_take_out_locks(self):
        with patch('pokedb.locks.get_locks_for_read') as mock_lock:
            access.read(1, 1)

        mock_lock.assert_called_once_with(1, 'main', [1])

    def test_fails_gracefully_if_read_lock_collision(self):
        with patch('pokedb.locks.get_locks_for_read', side_effect=LockException):
            response = access.read(1, 1)

        self.assertEqual(response, "Lock collision for read")

    def test_returns_none_if_data_does_not_exist(self):
        response = access.read(1, 1)
        self.assertEqual(response, {1: None})

    def test_returns_stored_value(self):
        storage._storage[1] = (['test'])
        storage._temp[2] = {1: 'updated'}
        response = access.read(1, 1)
        self.assertEqual(response, {1: {'value': 'test'}})

    def test_prefers_transaction_specific_value(self):
        storage._storage[1] = ('test'),
        storage._temp[2] = {1: ('updated',)}
        response = access.read(2, 1)
        self.assertEqual(response, {1: {'value': 'updated'}})

    def tearDown(self):
        storage._storage = dict()
        storage._temp = dict()

        locks.stop()

class TestWriteRow(unittest.TestCase):

    def setUp(self):
        storage._storage = dict()
        storage._temp = dict()
        storage._temp[1] = dict()
        storage._temp[2] = dict()

        locks.start()

    def test_calls_lock_module_to_take_out_locks(self):
        with patch('pokedb.locks.get_locks_for_write') as mock_lock:
            access.write(1, 1, 'test')

        mock_lock.assert_called_once_with(1, 'main', [1])
        
    def test_fails_gracefully_if_write_lock_collision(self):
        with patch('pokedb.locks.get_locks_for_write', side_effect=LockException):
            response = access.write(1, 1, 'test')

        self.assertEqual(response, "Lock collision for write")

    def test_does_not_write_over_main_table(self):
        storage._storage[1] = ('test',)
        storage._temp[2] = dict()
        response = access.write(2, 1, 'updated')
        self.assertEqual(storage._temp[2][1], ('updated',))
        self.assertEqual(storage._storage[1], ('test',))

    def tearDown(self):
        storage._storage = dict()
        storage._temp = dict()

        locks.stop()


class TestFinishWrite(unittest.TestCase):

    def setUp(self):
        storage._storage = dict()
        storage._temp = dict()
        storage._temp[1] = dict()
        storage._temp[2] = dict()

    def tearDown(self):
        storage._storage = dict()
        storage._temp = dict()

    def test_writes_to_main_storage(self):
        storage._storage[1] = 'test'
        storage._temp[2] = {1: 'updated'}

        access.finish_write(2)

        self.assertEqual(storage._storage[1], 'updated')
