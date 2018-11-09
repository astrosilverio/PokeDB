PAGE_SIZE = 4096


class Pager(object):

    def __init__(self, dbfile):
        self.dbfile = dbfile
        self.page_cache = dict()

    def get_page(self, page_num, force_fetch=False):
        if not force_fetch:
            cached_page = self.page_cache.get(page_num)
            if cached_page:
                return cached_page

        return self._fetch_page_from_disk(page_num=page_num)

    def _fetch_page_from_disk(self, page_num=0):
        with open(self.dbfile, 'r') as f:
            page_start = PAGE_SIZE * page_num
            f.seek(page_start)
            page = f.read(PAGE_SIZE)

        self.page_cache[page_num] = page

        return page

    def flush_page(self, page_num):
        page_contents = self.page_cache.get(page_num)

        if not page_contents:
            raise ValueError("No cached page {} to flush".format(page_num))
        if len(page_contents) > PAGE_SIZE:
            raise ValueError("Cached page {} has become too large".format(page_num))

        with open(self.dbfile, 'w') as f:
            page_start = PAGE_SIZE * page_num
            f.seek(page_start)
            f.write(page_contents)
            del self.page_cache[page_num]

    def db_close(self):
        """This is pretty dumb--the dict cache struct is unordered
        so there's probably too much seeking around, should time"""
        failed_pages = []
        for page_num in self.page_cache.keys():
            try:
                self.flush_page(page_num)
            except ValueError:
                failed_pages.append(page_num)

        if failed_pages:
            raise ValueError("Failed to write pages {}".format(failed_pages))
