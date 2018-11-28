"""
API from main process:
`read`
`write`
"""

# from pokedb.access.btree import build

# _btree = build_btree()

from pokedb import locks
from pokedb.locks.exceptions import LockException


# I AM A VISITOR HERE I AM NOT PERMANENT
_storage = dict()
_temp = dict()


def start():
    """Load btree"""
    pass


def start_txn(txn_id):
    _temp[txn_id] = dict()


def read(txn_id, row_id):
    try:
        locks.get_locks_for_read(txn_id, 'main', [row_id])
    except LockException:
        return "Lock collision for read"
    else:
        data = dict()
        data[row_id] = _storage.get(row_id, None)
        updated_value = _temp[txn_id].get(row_id, None)
        if updated_value:
            data[row_id] = updated_value
        return data


def write(txn_id, row_id, value):
    try:
        locks.get_locks_for_write(txn_id, 'main', [row_id])
    except LockException:
        return "Lock collision for write"
    else:
        _temp[txn_id][row_id] = value
        return 'ok'


def finish_write(txn_id):
    for row_id, value in _temp[txn_id].iteritems():
        _storage[row_id] = value
