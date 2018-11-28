import unittest

from pokedb.locks.exceptions import LockException
from pokedb.locks.manager import LockManager


class TestLockAcquisition(unittest.TestCase):

    def test_lock_acquired_with_txn_id_as_value(self):
        manager = LockManager()

        manager.acquire_lock(1, 'pokemon', 2)

        self.assertIn('pokemon.2', manager.locks.keys())
        self.assertEqual(manager.locks['pokemon.2'], 1)

    def test_does_not_raise_if_lock_already_acquired_by_same_txn(self):
        manager = LockManager()
        manager.acquire_lock(1, 'pokemon', 2)

        manager.acquire_lock(1, 'pokemon', 2)

        self.assertIn('pokemon.2', manager.locks.keys())
        self.assertEqual(manager.locks['pokemon.2'], 1)       

    def test_raises_if_lock_acquired_by_another_txn(self):
        manager = LockManager()
        manager.acquire_lock(1, 'pokemon', 2)

        with self.assertRaises(LockException):
            manager.acquire_lock(2, 'pokemon', 2)


class TestLockRelease(unittest.TestCase):

    def test_lock_release_deletes_lock(self):
        manager = LockManager()
        manager.locks['pokemon.2'] = 1

        manager.release_lock(1, 'pokemon', 2)

        self.assertIsNone(manager.locks.get('pokemon.2'))

    def test_raises_if_lock_does_not_exist(self):
        manager = LockManager()

        with self.assertRaises(LockException) as e:
            manager.release_lock(1, 'pokemon', 2)

        self.assertIn('does not exist', e.exception.message)

    def test_raises_if_txn_does_not_own_lock(self):
        manager = LockManager()
        manager.locks['pokemon.2'] = 1

        with self.assertRaises(LockException) as e:
            manager.release_lock(2, 'pokemon', 2)

        self.assertIn('does not own', e.exception.message)
