"""
From main process, three methods: `begin_transaction`, `commit`, `rollback`
"""

from pokedb.transactions.manager import Transaction, TransactionManager


__all__ = [
    'begin_transaction',
    'commit',
    'rollback',
]


_transaction_manager = None


def start():
    global _transaction_manager
    _transaction_manager = TransactionManager()


def begin_transaction():
    """Returns a transaction id. should it return a txn object?"""
    return _transaction_manager.begin_transaction()


def commit(txn_id):
    """Can raise a LockException if it cannot release its locks"""
    return _transaction_manager.commit(txn_id)


def rollback(txn_id):
    """Can raise a LockException if it cannot release its locks"""
    return _transaction_manager.rollback(txn_id)


def is_done(txn_id):
    return _transaction_manager.transaction_statuses.get(txn_id, None) == 'done'


def stop():
    global _transaction_manager
    del _transaction_manager
