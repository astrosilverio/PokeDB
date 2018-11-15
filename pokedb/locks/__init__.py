"""
API:
`acquire_lock`
`release_lock`
`get_locks_for_read`
`get_locks_for_write`
`release_locks_for_txn`
"""

from pokedb.locks.exceptions import LockException
from pokedb.locks.manager import LockManager


__all__ = [
    'acquire_lock',
    'release_lock',
    'release_locks_for_txn',
    'get_locks_for_read',
    'get_locks_for_write',
]


_lock_manager = None


def start():
    global _lock_manager
    _lock_manager = LockManager()


def acquire_lock(txn, table, row):
    """Acquire a row-level lock on a particular row in a particular table for a particular transaction.

    raises a LockException if the lock has been taken out by another transaction.
    """
    return _lock_manager.acquire_lock(txn, table, row)


def release_lock(txn, table, row):
    """Release a row-level lock.

    raises a LockException if the transaction does not own the lock or if the lock has already been released.
    """
    return _lock_manager.release_lock(txn, table, row)


def release_locks_for_txn(txn):
    """Release all locks held by a particular transaction"""
    return _lock_manager.release_locks_for_txn(txn)


def get_locks_for_read(txn, table, rows):
    return _lock_manager.get_locks_for_read(txn, table, rows)


def get_locks_for_write(txn, table, rows):
    return _lock_manager.get_locks_for_write(txn, table, rows)
