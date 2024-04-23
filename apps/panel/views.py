from django.http import Http404, HttpResponse
from mptt.templatetags.mptt_tags import *
###
from .models import Page, Slice
from .jinja.jinja_renderer import jinja_renderer
from .page_manager import  *
from .logger import log_page_tree 
from django.utils.text import slugify 
# Do the JavaScript magic to update slug field while typing title


def page_view(request, url):
    pm = Page.objects
    url = pm.extract_url(url)  # Extract the necessary part of the URL
    #pm.clear_cache()  # Ensure that clear_cache method exists
    #print(pm._build_url(page=page))
    
    #pm.rebuild_tree()
    logger.debug(f"Page: {url}")  #                                           #
    context = pm.build_page_context(url)
    #log_page_tree(page)
                                                #
    #parent_page_type = context.get('parent_page_type')  # Replace 'default_type' with your actual default
    #logger.debug(f"Parent_page_type type: {type(parent_page_type)}, value: {parent_page_type}")
    #current_level = int(context.get('current_level', 0)) # Convert levels to integers and add them to the context
    #start_level = int(context.get('start_level', 0))
    #end_level = int(context.get('end_level', 2))
                                          #
    #context.update({
    #    'current_level': current_level,
    #    'start_level': start_level,
    #    'end_level': end_level
    #})
    #logger.debug(f"current_level type: {type(current_level)}, value: {current_level}")
    #logger.debug(f"start_level type: {type(start_level)}, value: {start_level}")
    #logger.debug(f"end_level type: {type(end_level)}, value: {end_level}")
                                                #
    env = jinja_renderer()
    template = env.get_template('panel/jinja/jinja_page_manager.html')
    rendered_template = template.render(context)
    return HttpResponse(rendered_template)

                                                #


def pm_view(request, url=None):
    pm = Page.objects
    extracted_url = pm.extract_url(url)  # Extract the necessary part of the URL
    page = pm.get_page_by_url(extracted_url)  # Retrieve the page by the extracted URL
    if page is None:
        raise Http404(f"Page not found for URL: {extracted_url}")
    # Log the page tree if necessary (function not shown here)
    log_page_tree(page)
    context = pm.build_page_context(url=extracted_url, page=page)
    env = jinja_renderer()
    template = env.get_template('panel/jinja/jinja_page_manager.html')
    rendered_template = template.render(context)
    return HttpResponse(rendered_template)
    

    
def test_view(request):
    try:
        result = Page.objects.get_active_pages_dict()
        return HttpResponse(str(result))
    except AttributeError as e:
        return HttpResponse("AttributeError: " + str(e))