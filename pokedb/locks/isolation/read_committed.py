def get_read_locks(transaction, table, rows, lock_manager):
    return


def get_write_locks(transaction, table, rows, lock_manager):
    for row in rows:
        lock_manager.acquire_lock(transaction.id, table, row)
