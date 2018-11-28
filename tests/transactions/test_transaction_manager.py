import unittest
from mock import patch

from pokedb import access, locks
from pokedb.locks.exceptions import LockException
from pokedb.transactions.constants import (
    TXN_IN_PROGRESS,
    TXN_COMMITTING,
    TXN_ABORTED,
    TXN_ROLLBACK,
    TXN_DONE)
from pokedb.transactions.exceptions import TransactionStatusError
from pokedb.transactions.manager import Transaction, TransactionManager


class TestBeginTransaction(unittest.TestCase):

    def setUp(self):
        self.manager = TransactionManager()

    def test_assigns_incremental_txn_id(self):
        initial_next_id = self.manager.next_txn_id

        txn_id = self.manager.begin_transaction()

        self.assertEqual(txn_id, initial_next_id)
        self.assertEqual(self.manager.next_txn_id, initial_next_id+1)

    def test_creates_in_progress_transaction(self):
        txn_id = self.manager.begin_transaction()
        self.assertEqual(self.manager.transaction_statuses[txn_id], TXN_IN_PROGRESS)

    def test_creates_txn_object(self):
        txn_id = self.manager.begin_transaction()

        txn_object = self.manager.transactions[txn_id]
        self.assertEqual(txn_object.__class__, Transaction)
        self.assertEqual(txn_object.id, txn_id)

    def test_creates_temp_storage_for_txn(self):
        txn_id = self.manager.begin_transaction()

        self.assertEqual(access._temp[txn_id], dict())


class TestCommitTransaction(unittest.TestCase):

    def setUp(self):
        self.manager = TransactionManager()
        locks.start()

    def tearDown(self):
        locks.stop()

    def test_raises_if_txn_is_already_aborted(self):
        txn_id = self.manager.begin_transaction()
        self.manager.transaction_statuses[txn_id] = TXN_ABORTED

        with self.assertRaises(TransactionStatusError):
            self.manager.commit(txn_id)

        self.assertEqual(self.manager.transaction_statuses[txn_id], TXN_ABORTED)

    def test_raises_if_txn_is_already_committed(self):
        txn_id = self.manager.begin_transaction()
        self.manager.transaction_statuses[txn_id] = TXN_DONE

        with self.assertRaises(TransactionStatusError):
            self.manager.commit(txn_id)

        self.assertEqual(self.manager.transaction_statuses[txn_id], TXN_DONE)

    def test_does_not_move_txn_to_done_status_if_locks_not_released(self):
        txn_id = self.manager.begin_transaction()

        with patch('pokedb.transactions.manager.release_locks_for_txn', side_effect=LockException):
            self.manager.commit(txn_id)

        self.assertEqual(self.manager.transaction_statuses[txn_id], TXN_COMMITTING)

    def test_releases_locks_taken_out_by_txn(self):
        txn_id = self.manager.begin_transaction()
        other_txn_id = txn_id + 1
        locks.acquire_lock(txn_id, 'pokemon', 1)
        locks.acquire_lock(other_txn_id, 'pokemon', 2)
        total_locks_for_txn = len([v for v in locks._lock_manager.locks.values() if v == txn_id])
        total_locks = len(locks._lock_manager.locks.values())
        self.assertEqual(total_locks_for_txn, 1)
        self.assertEqual(total_locks, 2)

        self.manager.commit(txn_id)

        total_locks_for_txn = len([v for v in locks._lock_manager.locks.values() if v == txn_id])
        total_locks = len(locks._lock_manager.locks.values())
        self.assertEqual(total_locks_for_txn, 0)
        self.assertEqual(total_locks, 1)

    def test_moves_txn_to_done_status_if_locks_released_successfully(self):
        txn_id = self.manager.begin_transaction()
        locks.acquire_lock(txn_id, 'pokemon', 1)

        self.manager.commit(txn_id)

        self.assertEqual(self.manager.transaction_statuses[txn_id], TXN_DONE)

    def test_finishes_write_with_storage(self):
        txn_id = self.manager.begin_transaction()

        with patch('pokedb.access.finish_write') as mock_finish:
            self.manager.commit(txn_id)

        mock_finish.assert_called_once_with(txn_id)

    def test_does_not_finish_write_with_storage_if_locks_not_released(self):
        txn_id = self.manager.begin_transaction()

        with patch('pokedb.transactions.manager.release_locks_for_txn', side_effect=LockException):
            with patch('pokedb.access.finish_write') as mock_finish:
                self.manager.commit(txn_id)

        mock_finish.assert_not_called()


class TestRollbackTransaction(unittest.TestCase):

    def setUp(self):
        self.manager = TransactionManager()
        locks.start()

    def tearDown(self):
        locks.stop()

    def test_raises_if_transaction_is_already_aborted(self):
        txn_id = self.manager.begin_transaction()
        self.manager.transaction_statuses[txn_id] = TXN_ABORTED

        with self.assertRaises(TransactionStatusError):
            self.manager.rollback(txn_id)

        self.assertEqual(self.manager.transaction_statuses[txn_id], TXN_ABORTED)

    def test_raises_if_transaction_is_already_committed(self):
        txn_id = self.manager.begin_transaction()
        self.manager.transaction_statuses[txn_id] = TXN_DONE

        with self.assertRaises(TransactionStatusError):
            self.manager.rollback(txn_id)

        self.assertEqual(self.manager.transaction_statuses[txn_id], TXN_DONE)

    def test_does_not_move_txn_to_aborted_status_if_locks_not_released(self):
        txn_id = self.manager.begin_transaction()

        with patch('pokedb.transactions.manager.release_locks_for_txn', side_effect=LockException):
            self.manager.rollback(txn_id)

        self.assertEqual(self.manager.transaction_statuses[txn_id], TXN_ROLLBACK)

    def test_releases_all_locks_taken_out_by_txn(self):
        txn_id = self.manager.begin_transaction()
        other_txn_id = txn_id + 1
        locks.acquire_lock(txn_id, 'pokemon', 1)
        locks.acquire_lock(other_txn_id, 'pokemon', 2)
        total_locks_for_txn = len([v for v in locks._lock_manager.locks.values() if v == txn_id])
        total_locks = len(locks._lock_manager.locks.values())
        self.assertEqual(total_locks_for_txn, 1)
        self.assertEqual(total_locks, 2)

        self.manager.rollback(txn_id)

        total_locks_for_txn = len([v for v in locks._lock_manager.locks.values() if v == txn_id])
        total_locks = len(locks._lock_manager.locks.values())
        self.assertEqual(total_locks_for_txn, 0)
        self.assertEqual(total_locks, 1)

    def test_moves_txn_to_aborted_status_if_locks_released_successfully(self):
        txn_id = self.manager.begin_transaction()
        locks.acquire_lock(txn_id, 'pokemon', 1)

        self.manager.rollback(txn_id)

        self.assertEqual(self.manager.transaction_statuses[txn_id], TXN_ABORTED)
