#apps\panel\cached_trees.py
from mptt.templatetags.mptt_tags import get_cached_trees
from mptt.managers import TreeManager


class PageManager(TreeManager):
    def get_active_pages(self):
        # Use TreeQuerySet's get_cached_trees() method directly
        return get_cached_trees(self.filter(state='active').order_by('tree_id', 'lft').prefetch_related('slices'))

    def get_child_pages(self, parent_page):
        # This method doesn't need to change because it's already efficient
        # It retrieves children for a single parent, presumably already fetched
        return parent_page.get_children().filter(state='active')

    def get_page_by_url(self, url):
        if url is None:
            # Handle the case where URL is None
            return None  # or raise an exception
        # Use get_cached_trees to retrieve and cache all active pages with their hierarchy
        cached_pages = get_cached_trees(self.filter(state='active').order_by('tree_id', 'lft').prefetch_related('slices'))
        # Iterate through the cached pages to find the one with the given URL
        for page in cached_pages:
            if page.url == url:
                return page
            for descendant in page.get_descendants():
                if descendant.url == url:
                    return descendant
        return None  # If no page is found with the URL, return None

