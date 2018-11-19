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


def start():
    global _pager
    _pager = Pager(DBFILE)


def get_row(row_id, page_num):
    page = _pager.get_page(page_num)
    return page  # notttttt at all what it should be


def write_row(row_id, data, page_num):
    page = _pager.get_page(page_num)
    return page  # NOPE


def sync(page_num):
    _pager.flush_page(page_num)
    return page_num


def stop():
    if _pager:
        return _pager.db_close()
