# debug_panel.py
import os
import django

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.base')
django.setup()

# Now you can safely import Django and MPTT models
#from mptt.models import MPTTModel, TreeForeignKey
from apps.panel.models import Page

# Import the functions from context_processors.py
from apps.panel.templatetags.context_processors import (
    build_url,
    find_page_by_attribute,
    fetch_slice_data,
    fetch_page_data,
    build_menu_item,
    get_menu_structure,
    process_breadcrumbs,
    get_current_page,
    get_page_context,
    get_current_page_data,
    page_to_dict,
    get_tree_data,
    serialize_tree
)


# Import the Page model
from apps.panel.models import Page
import time
# Define your debug_data function
import time  # Import the time module

class Debugger:
    @staticmethod
    def debug_data(data, debug_message, pause_duration=1.5):
        print(f"DEBUG: {debug_message}:")
        data_type = type(data).__name__
        
        if isinstance(data, list):
            print(f"  List of {len(data)} items")
            for item in data:
                print(f"   - {type(item).__name__}: {item}")
        elif isinstance(data, dict):
            print(f"  Dict with {len(data)} keys:")
            for key, value in data.items():
                print(f"   - {key} ({type(value).__name__}): {value}")
        else:
            print(f" *  {data_type}: {data}")

        time.sleep(pause_duration)  # Pause for the specified duration

    # Now, you can use the Debugger class and it will automatically pause after each debug output

    @classmethod
    def add(cls, data, message):
        cls.debug_data(data, message)

# Now, define a function to run all your debug functions
def run_debug():
    # Get the active pages from the database (Expected output: QuerySet of Page objects)
    cached_pages = Page.objects.get_active_pages()
    Debugger.add(cached_pages, "Cached Pages")
    # Create a dictionary mapping page URLs to page objects (Expected output: Dict[str, Page])
    page_dict = {page.url: page for page in cached_pages}
    Debugger.add(page_dict, "Page Dictionary" )
    # Define root_nodes here using the get_root_nodes method (Change #1)
    root_nodes_queryset = Page.objects.root_nodes()
    Debugger.add(root_nodes_queryset, "Root Nodes")

    # Assume 'comby' is a placeholder for an actual page URL you wish to debug
    current_page_url = 'comby'
    current_page = page_dict.get(current_page_url)

    # Get the menu structure using the root nodes queryset (Change #2)
    menu_structure = get_menu_structure(root_nodes_queryset, current_page, page_dict)
    Debugger.add(menu_structure, "Menu Structure")

    # Get and debug the page context for the current page URL (Expected output: Dict[str, Any])
    context = get_page_context(page_dict, current_page_url)
    Debugger.add(context, f"Page Context for URL '{current_page_url}'")

    # Debug breadcrumbs if needed (Expected output: List[Dict[str, Any]])
    breadcrumbs = process_breadcrumbs(current_page, page_dict)
    Debugger.add(breadcrumbs, "Breadcrumbs")

   # Using 'build_url' function and debugging the result
    if current_page:
        url = build_url(current_page)
        Debugger.add(url, f"URL for {current_page.title}")

    # Using 'find_page_by_attribute' function and debugging the result
    page_by_attribute = find_page_by_attribute(page_dict, 'url', current_page_url)
    Debugger.add(page_by_attribute, f"Page found by attribute for URL '{current_page_url}'")

    # Using 'fetch_slice_data' function and debugging the result
    if current_page:
        slice_data = fetch_slice_data(current_page)
        Debugger.add(slice_data, f"Slice data for {current_page.title}")

    # Using 'fetch_page_data' function and debugging the result
    if current_page:
        page_data = fetch_page_data(current_page)
        Debugger.add(page_data, f"Page data for {current_page.title}")

    # Using 'build_menu_item' function and debugging the result
    # Note: 'build_menu_item' is used within 'get_menu_structure', so it will be debugged there
    # ...

    # Using 'serialize_tree' function and debugging the result
    tree_data = serialize_tree(root_nodes_queryset, page_dict)
    Debugger.add(tree_data, "Serialized Tree Data")

    # Using 'get_current_page' function and debugging the result
    current_page_from_url = get_current_page(page_dict, current_page_url)
    Debugger.add(current_page_from_url, f"Current page from URL '{current_page_url}'")

    # Using 'get_current_page_data' function and debugging the result
    current_page_data, _ = get_current_page_data(page_dict, current_page_url)
    Debugger.add(current_page_data, f"Current page data for URL '{current_page_url}'")

# Call run_debug if this script is executed directly
if __name__ == '__main__':
    run_debug()