from pokedb.locks.exceptions import LockException
from pokedb.locks.isolation import get_read_locks, get_write_locks


class LockManager(object):

    def __init__(self):
        self.locks = dict()

    def _get_lock_key(self, table, row):
        return "{table}.{row}".format(table=table, row=row)

    def acquire_lock(self, txn_id, table, row):
        lock_key = self._get_lock_key(table, row)
        lock_value = self.locks.get(lock_key)
        if not lock_value:
            self.locks[lock_key] = txn_id
            return
        elif lock_value and lock_value == txn_id:
            return
        else:
            raise LockException('lock already taken out')

    def release_lock(self, txn_id, table, row):
        lock_key = self._get_lock_key(table, row)
        lock_value = self.locks.get(lock_key)
        if not lock_value:
            raise LockException('lock does not exist')

        elif lock_value and lock_value != txn_id:
            raise LockException('txn does not own this lock')

        else:
            del self.locks[lock_key]

    def release_locks_for_txn(self, txn_id):
        lock_keys = [k for k, v in self.locks.iteritems() if v == txn_id]
        for lock_key in lock_keys:
            del self.locks[lock_key]

    def get_locks_for_read(self, txn_id, table, rows):
        return get_read_locks(txn_id, table, rows, self)

    def get_locks_for_write(self, txn_id, table, rows):
        return get_write_locks(txn_id, table, rows, self)
