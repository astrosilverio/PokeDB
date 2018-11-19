"""
API to access layer:
`get`
`write`
`sync`
"""

import os

from pokedb.storage.pager import Pager


DBFILE = os.getenv('DBFILE', 'test.db')

_pager = None


# In-memory storage
_storage = dict()
_temp = dict()


def start():
    global _pager
    _pager = Pager(DBFILE)


def get_row(txn_id, row_id, page_num):
    data = dict()
    data[row_id] = _storage.get(row_id, None)
    updated_value =  _temp[txn_id].get(row_id, None)
    if updated_value:
        data[row_id] = updated_value
    return data


def write_row(txn_id, row_id, data, page_num):
    _temp[txn_id][row_id] = value
    return page_num


def sync(page_num):
    _pager.flush_page(page_num)
    return page_num


def stop():
    if _pager:
        return _pager.db_close()
