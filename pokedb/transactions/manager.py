from pokedb.locks import release_locks_for_txn
from pokedb.locks.exceptions import LockException
from pokedb.transactions.constants import TXN_IN_PROGRESS, TXN_COMMITTING, TXN_ABORTED, TXN_ROLLBACK, TXN_DONE
from pokedb.transactions.exceptions import TransactionStatusError


class Transaction(object):

    def __init__(self, id):
        self.id = id
        self.statements = []
        self.allowed_versions = []


class TransactionManager(object):

    def __init__(self):
        self.next_txn_id = 1
        self.transactions = dict()
        self.transaction_statuses = dict()

    def begin_transaction(self):
        new_txn_id = self.next_txn_id
        self.next_txn_id += 1

        txn = Transaction(new_txn_id)
        response = new_txn_id

        self.transactions[new_txn_id] = txn
        self.transaction_statuses[new_txn_id] = TXN_IN_PROGRESS
        from pokedb.access import start_txn
        start_txn(new_txn_id)
        return response

    def commit(self, txn_id):
        if not self.transaction_statuses[txn_id] == TXN_IN_PROGRESS:
            raise TransactionStatusError("why are you trying to commit this")

        self.transaction_statuses[txn_id] = TXN_COMMITTING
        txn = self.transactions[txn_id]

        try:
            release_locks_for_txn(txn.id)
        except LockException as e:
            response = "could not release locks"
        else:
            response = "committed"
        from pokedb.access import finish_write
        self.transaction_statuses[txn_id] = TXN_DONE
        finish_write(txn_id)
        return response

    def rollback(self, txn_id):
        if not self.transaction_statuses[txn_id] in [TXN_IN_PROGRESS, TXN_COMMITTING]:
            raise TransactionStatusError("why are you trying to roll this back")

        self.transaction_statuses[txn_id] = TXN_ROLLBACK
        txn = self.transactions[txn_id]

        try:
            release_locks_for_txn(txn.id)
        except LockException as e:
            response = "could not release locks"
        else:
            response = "aborted"

        self.transaction_statuses[txn_id] = TXN_ABORTED
        return response
