# apps\panel\logger.py
import logging
import json

logger = logging.getLogger(__name__)

# - %(levelname)s 

#how to add some outline when each starts



logging.basicConfig(

    level=logging.DEBUG,
    format='-------------------------------------------------------------------------------------------------------------------------------------------------\n%(levelname)s - %(asctime)s - %(funcName)s - %(message)s',
    datefmt='%d %H:%M:%S',
    handlers=[
        logging.StreamHandler()  # This will print to console
    ]
)
#logging.basicConfig(
#    level=logging.DEBUG,
#    format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
#    datefmt='%Y-%m-%d %H:%M:%S'
#)




def log_page_tree(page, level=0):
    children = getattr(page, 'get_children', lambda: [])()
    slices = []
    if hasattr(page, 'slices'):
        slices = page.slices.all()
    # Convert complex types to serializable formats
    slices_info = [
        {
            'title': slice.title,
            'state': str(slice.state),  # Convert state to string
            'price': str(slice.price),  # Ensure price is a string, in case it's a Decimal or other type
            'text': slice.text,
            'timestamp': slice.timestamp.isoformat() if slice.timestamp else None,  # Convert datetime to ISO format
            'icon': slice.icon.url if slice.icon else None,
        }
        for slice in slices
    ]

    log_entry = {
        'page_title': page.title,
        'page_url': getattr(page, 'url', ''),
        'level': level,
        'children_titles': [child.title for child in children],
        'slices_info': slices_info
    }

    # Serialize log_entry to JSON and log it
    logger.debug(json.dumps(log_entry, ensure_ascii=False, indent=2))

    # Recursively log children
    for child in children:
        log_page_tree(child, level + 1)

