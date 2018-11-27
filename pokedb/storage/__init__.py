"""
API to access layer:
`get`
`write`
`sync`
"""

import os

from pokedb.storage.pager import Pager
from pokedb.storage.serializer import serialize, deserialize


DBFILE = os.getenv('DBFILE', 'test.db')

_pager = None


# In-memory storage
_storage = dict()
_temp = dict()
_table_schema = {
    'main': ('value'),
}


def start():
    global _pager
    _pager = Pager(DBFILE)


def get_row(txn_id, table, row_id, page_num):
    raw_data = _storage.get(row_id, None)
    updated_value =  _temp[txn_id].get(row_id, None)
    if updated_value:
        raw_data = updated_value
    schema = _table_schema.get(table)
    data = deserialize(schema, raw_data)
    return data


def write_row(txn_id, table, row_id, data, page_num):
    schema = _table_schema.get(table)
    raw_data = serialize(schema, data)
    _temp[txn_id][row_id] = raw_data
    return page_num


def sync(page_num):
    _pager.flush_page(page_num)
    return page_num


def stop():
    if _pager:
        return _pager.db_close()
