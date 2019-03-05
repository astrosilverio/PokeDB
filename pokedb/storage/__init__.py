"""
API to access layer:
`get`
`write`
`sync`
"""

import os

from pokedb.schema import serialize, deserialize
from pokedb.storage.pager import Pager


DBFILE = os.getenv('DBFILE', 'test.db')

_pager = None


# In-memory storage
_storage = dict()
_temp = dict()

def start():
    global _pager
    _pager = Pager(DBFILE)


def get_row(txn_id, table, row_id, page_num):
    raw_data = _storage.get(row_id, None)
    updated_value =  _temp[txn_id].get(row_id, None)
    if updated_value:
        raw_data = updated_value
    if raw_data:
        data = deserialize(table, raw_data)
    else:
        data = None
    return {row_id: data}


def write_row(txn_id, table, row_id, data, page_num):
    fmt = _table_schema.get(table)
    raw_data = serialize(fmt, *data)
    _temp[txn_id][row_id] = raw_data
    return page_num


def sync(page_num):
    _pager.flush_page(page_num)
    return page_num


def stop():
    if _pager:
        return _pager.db_close()
