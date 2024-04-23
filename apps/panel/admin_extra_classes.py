from django.contrib import admin
from apps.panel.models import Slice, Page, Website
from apps.panel.model_extra_classes import Media, TextContent, Template, Set, SEOData
from config.base import BASE_DIR

# Admin class for Media
@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'alt', 'uploaded_at')
    search_fields = ('title', 'alt')


# Admin class for TextContent
@admin.register(TextContent)
class TextContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'content_type')
    search_fields = ('title',)

@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ('name', 'items_content_type', 'items_object_id')
    search_fields = ('name', 'items_object_id')
    change_form_template = str(BASE_DIR / 'templates/panel/admin/ContentTypesForm.html')

    class Media:
        js = ('js/get_set_objects.js',)  # Correct way to include JavaScript files

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "items_object_id":
            # Your logic to customize the form field
            slice_objects = Slice.objects.all()
            media_objects = Media.objects.all()
            template_objects = Template.objects.all()
            # Combine the item objects from all models
            all_items = list(slice_objects) + list(media_objects) + list(template_objects)
            kwargs["queryset"] = all_items
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    

admin.site.register(SEOData)
class SEODataAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')