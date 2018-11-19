import os

from pokedb.locks.isolation import read_committed

ISOLATION_RULES = {
    'READ_COMMITTED': read_committed
}

ISOLATION_LEVEL = os.getenv('ISOLATION_LEVEL', 'READ_COMMITTED')

get_read_locks = ISOLATION_RULES[ISOLATION_LEVEL].get_read_locks
get_write_locks = ISOLATION_RULES[ISOLATION_LEVEL].get_write_locks

