from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from config import base
from django.conf.urls.static import static
from django.http import HttpResponseNotFound
#from django import request

from apps.panel.views import *
#from apps.panel.admin.admin_views import * #moved to c:/Users/User/Desktop/Nest/DEV/apps/panel/admin_views.py
from apps.panel.admin_views import get_objects
#from apps.panel import admin_views


urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    #path('admin/', admin.site.urls),
    path('admin/', admin.site.urls),
    path('get_set_objects/', get_objects, name='get_set_objects'),
    path('<path:url>/', page_view, name='page-detail'),
    #path('favicon.ico', lambda request: HttpResponseNotFound()),
    path('tinymce/', include('tinymce.urls')),
    
    #path('admin/get_set_objects/', get_objects, name='get_objects'),
    #path('media/', media_view, name='media'),
    #path('menu/', filtered_menu_view, name='menu'),
    #path('test/', test_view, name='test_view'),
    #path('debug/<path:url>/', debug_view, name='debug-view'), #path('<path:url>/', full_view, name='page-detail'), name='page-detail' means what is used in the menu
   # path('pm/', pm_view, name='pm_view'),  # For when no URL is provided
   # path('pm/<path:url>', pm_view, name='pm_view'),  # For when a URL is provided
    

] + static(base.MEDIA_URL, document_root=base.MEDIA_ROOT)

if base.DEBUG:
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
    urlpatterns += static(base.MEDIA_URL, document_root=base.MEDIA_ROOT)
