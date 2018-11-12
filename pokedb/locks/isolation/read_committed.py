def get_read_locks(transaction, rows, lock_manager):
    return


def get_write_locks(transaction, rows, lock_manager):
    for row in rows:
        lock_manager.acquire_lock(transaction.id, 'main', row)
