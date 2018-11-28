"""
API from main process:
`read`
`write`
"""

# from pokedb.access.btree import build

# _btree = build_btree()

from pokedb import locks, storage
from pokedb.locks.exceptions import LockException


def start():
    """Load btree"""
    pass


def start_txn(txn_id):
    storage._temp[txn_id] = dict()


def read(txn_id, row_id):
    try:
        locks.get_locks_for_read(txn_id, 'main', [row_id])
    except LockException:
        return "Lock collision for read"
    else:
        data = storage.get_row(txn_id, 'main', row_id, 1)
        return data


def write(txn_id, row_id, value):
    try:
        locks.get_locks_for_write(txn_id, 'main', [row_id])
    except LockException:
        return "Lock collision for write"
    else:
        storage.write_row(txn_id, 'main', row_id, {'value': value}, 1)
        return 'ok'


def finish_write(txn_id):
    for row_id, value in storage._temp[txn_id].iteritems():
        storage._storage[row_id] = value
