from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from django.utils.html import format_html
from django.urls import reverse
from .models import Page, Website, Slice
#from apps.panel.admin.admin_extra_classes import *

@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin, ):
    list_display = ('name', 'url', 'state', 'type', 'owner')
    search_fields = ('name', 'url')
    
# Admin class for Page
@admin.register(Page)
class PageAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions',  'indented_title', 'url', 'type',  'state',)
    list_display_links = ('indented_title',)
    mptt_indent_field = "title"
    search_fields = ('title', 'url')

# Admin class for Slice
@admin.register(Slice)
class SliceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image_tag', 'get_parent_page_title', 'price', 'state')
    list_filter = ('parent_page',)
    readonly_fields = ('image_tag',)
    def image_tag(self, obj):
        if obj.img and obj.img.name.endswith('.svg'):
            # Uncomment the following line to sanitize SVG uploads
            #obj.img = sanitize_svg_upload(obj.img)
            return format_html('<img src="{}" width="50" />', obj.img.url)
        return "No Image"
    image_tag.short_description = 'Image Preview'

    def get_parent_page_title(self, obj):
        return obj.parent_page.title if obj.parent_page else None
    get_parent_page_title.short_description = 'Parent Page Title'

    def add_child_slice_link(self, obj):
        url = reverse('admin:panel_slice_add') + f"?parent_page={obj.pk}"
        return format_html('<a href="{}">Add Child Slice</a>', url)
    add_child_slice_link.short_description = 'Add Child Slice'

    def get_changeform_initial_data(self, request):
        initial_data = super().get_changeform_initial_data(request)
        parent_page_id = request.GET.get('parent_page')
        if parent_page_id:
            initial_data['parent_page'] = parent_page_id
        return initial_data


#from apps.panel.admin_extra_classes import *

