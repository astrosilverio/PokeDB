import os
import unittest
from mock import patch

from pokedb.storage import pager


class TestPager(unittest.TestCase):

    def setUp(self):
        """Create a file with almost 10000 bytes"""
        self.TEST_DBFILE = 'test.pkdb'
        with open(self.TEST_DBFILE, 'w') as f:
            f.write(str([i for i in range(5000)]))

        self.pager = pager.Pager(self.TEST_DBFILE)

    def tearDown(self):
        os.remove(self.TEST_DBFILE)

    def test_gets_PAGE_SIZE_bytes_from_file(self):
        """Test file contains a str type so we expect a
        str of length PAGE_SIZE"""
        page = self.pager.get_page(0)
        self.assertEqual(len(page), pager.PAGE_SIZE)

    def test_starts_at_correct_offset(self):
        """4096 chars (remember this is a str) from 0 starts at 841"""
        page = self.pager.get_page(1)
        self.assertTrue(page.startswith('841'))

    def test_prefers_cache_to_accessing_file(self):
        cached_data = "the answer is 42"
        self.pager.page_cache[0] = cached_data

        page = self.pager.get_page(0)

        self.assertEqual(page, cached_data)

    def test_fetching_from_disk_populates_cache(self):
        for i in range(2):
            page = self.pager.get_page(i)
            self.assertEqual(self.pager.page_cache[i], page)

    def test_force_fetching_from_disk_populates_cache(self):
        cached_data = "the question is what is 6 times 8"
        for i in range(2):
            self.pager.page_cache[i] = cached_data
            page = self.pager.get_page(i, force_fetch=True)
            self.assertEqual(self.pager.page_cache[i], page)

    def test_flush_writes_pages(self):
        cached_page = "the answer is 42"
        for i in range(2):
            self.pager.page_cache[i] = cached_page
            self.pager.flush_page(i)
            self.assertEqual(self.pager.get_page(i), cached_page)

    def test_flush_clears_cache(self):
        cached_page = "the answer is 42"
        for i in range(2):
            self.pager.page_cache[i] = cached_page
            self.pager.flush_page(i)
            self.assertEqual(self.pager.page_cache.get(i), None)        

    def test_flush_raises_if_no_cached_page_to_flush(self):
        for i in range(2):
            with self.assertRaises(ValueError) as e:
                self.pager.flush_page(i)
            self.assertEqual(e.exception.message, "No cached page {} to flush".format(i))

    def test_flush_raises_if_page_is_too_big(self):
        cached_page = "the answer is 42"
        self.pager.page_cache[0] = cached_page
        with patch('pokedb.storage.pager.pager.PAGE_SIZE', 10):
            with self.assertRaises(ValueError) as e:
                self.pager.flush_page(0)

        self.assertEqual(e.exception.message, "Cached page 0 has become too large")

    # def test_db_close_writes_all_pages_in_cache(self):
    #     cached_page_zero = "the answer is 42"
    #     cached_page_one = "the question is what is 6 times 8"
    #     self.pager.page_cache[0] = cached_page_zero
    #     self.pager.page_cache[1] = cached_page_one

    #     self.pager.db_close()

    #     self.assertEqual(self.pager.get_page(0), cached_page_zero)
    #     self.assertEqual(self.pager.get_page(1), cached_page_one)
