import jinja2
import config.base as base
from jinja2 import Environment
from django.templatetags.static import static
from django.urls import reverse

def jinja_renderer(**options):
    # Set default loader if not specified
    if 'loader' not in options:
        options['loader'] = jinja2.FileSystemLoader(base.TEMPLATES_DIR)
        print("Jinja2 search path:", options['loader'].searchpath)
    # Create the Jinja2 environment with options
    env = Environment(**options)
    # Update the environment with Django-specific globals
    env.globals.update({
        'static': static,
        'url': reverse,
    })
    # Add the MPTT-related globals
    #env.globals.update(get_cached_trees())
    return env