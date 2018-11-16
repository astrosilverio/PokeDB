def get_read_locks(transaction_id, table, rows, lock_manager):
    return


def get_write_locks(transaction_id, table, rows, lock_manager):
    for row in rows:
        lock_manager.acquire_lock(transaction_id, table, row)
