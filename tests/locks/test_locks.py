import unittest

from pokedb import locks


class TestLockStartup(unittest.TestCase):

    def test_lock_module_starting_creates_lock_manager(self):
        self.assertIsNone(locks._lock_manager)

        locks.start()

        self.assertIsNotNone(locks._lock_manager)
        self.assertEqual(locks._lock_manager.__class__, locks.LockManager)
