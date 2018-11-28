import unittest

from pokedb import locks, transactions


class TestTransactionStart(unittest.TestCase):

    def tearDown(self):
        transactions.stop()

    def test_start_creates_transaction_manager(self):
        self.assertIsNone(transactions._transaction_manager)

        transactions.start()

        self.assertIsNotNone(transactions._transaction_manager)
        self.assertEqual(transactions._transaction_manager.__class__, transactions.TransactionManager)


class TestTransactionStatusCheck(unittest.TestCase):

    def setUp(self):
        locks.start()
        transactions.start()

    def tearDown(self):
        locks.stop()
        transactions.stop()

    def test_is_done_is_true_for_done_transactions(self):
        txn_id = transactions.begin_transaction()
        transactions.commit(txn_id)

        self.assertTrue(transactions.is_done(txn_id))

    def test_is_done_is_false_for_aborted_transactions(self):
        txn_id = transactions.begin_transaction()
        transactions.rollback(txn_id)

        self.assertFalse(transactions.is_done(txn_id))

    def test_is_done_is_false_for_in_progress_transactions(self):
        txn_id = transactions.begin_transaction()

        self.assertFalse(transactions.is_done(txn_id))
