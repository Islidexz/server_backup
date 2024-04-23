from tinymce.models import HTMLField
from config.base import MEDIA_ROOT
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
###
from mptt.templatetags.mptt_tags import *
from apps.panel.page_manager import *
from .utils import *
from django.core.validators import FileExtensionValidator
from django.core.files.storage import FileSystemStorage

#from .admin_actions import *
#from .model_utils import *
####

#the structure is like this, each page has slices
#each page or slice can have multiple mediasets, and probably meadiasets will have their own order in a a page\slice
#we cannot have 2 same meadiasets or meadia in a mediaset for a unique page or slice
#extend this tech and upgrade, add more on whats needed


#each page has templateSets, and probably templateSets will have their own order in a a page
#each set has multiple templates for a unique page. also a small template is set for a slice
#the main template is set for a page, that holds the blocks with the slices set and
# their respective templates and order

#a slice can be related to different sets
# a media can be related to different sets
#should we be using a model like ordering?
lets dry and upgrade the models senior way

class OrderedModel(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField(default=0, db_index=True, help_text='Ordering position')

    class Meta:
        abstract = True
        ordering = ['order']

    def __str__(self):
        return self.title or "Unnamed Item"
    


##
file_storage = FileSystemStorage(location=os.path.join(MEDIA_ROOT, 'files'))
file_validator = FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)


class ContentObject(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True

class Set(models.Model):
    name = models.CharField(max_length=255)
    items_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    items_object_id = models.PositiveIntegerField()
    items = GenericForeignKey('items_content_type', 'items_object_id')
    order = models.JSONField(blank=True, null=True)  # Store the order of items
    def __str__(self):
        return self.name
    
    def get_ordered_items(self):
        # Assuming 'order' is a list of IDs representing the order of items
        item_model = self.items_content_type.model_class()
        ordered_ids = self.order or []
        return item_model.objects.filter(id__in=ordered_ids).order_by(
            models.Case(*[models.When(id=id, then=pos) for pos, id in enumerate(ordered_ids)])
        )
    
class SEOData(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    #parent_page = models.OneToOneField(Page, on_delete=models.SET_NULL, blank=True, null=True, related_name='seo_data')
    title = models.CharField(max_length=255, blank=True, null=True, help_text='SEO title')
    description = models.TextField(blank=True, null=True, help_text='Meta description for SEO')
    keywords = models.CharField(max_length=255, blank=True, null=True, help_text='Comma-separated keywords for SEO')
    slug = models.SlugField(max_length=255, blank=True, null=True, help_text='SEO-friendly URL')
    def __str__(self):
        return self.title or "SEO Data"
    #    seo_data = models.OneToOneField(SEOData, on_delete=models.SET_NULL, blank=True, null=True, related_name='page')


    
class Media(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    alt = models.CharField(max_length=255, blank=True, null=True)  # Mainly for images
    file = models.FileField(
        storage=file_storage,
        upload_to=upload_to,
        validators=[file_validator]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if self.file.name.endswith('.svg'):
            self.file = process_svg(self.file)
        super().save(*args, **kwargs)

class TextContent(models.Model):
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')
    title = models.CharField(max_length=255, blank=True, null=True)
    text = HTMLField(blank=True, null=True)
    keywords_block = models.TextField(blank=True, null=True)
    def __str__(self):
        title_display = f"Title: {self.title}" if self.title else "No Title"
        return f"TextContent for {self.content_type.model} ({title_display}): {self.text[:30]}..."

class Template(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()
    parent_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    parent_object_id = models.PositiveIntegerField()
    parent = GenericForeignKey('parent_content_type', 'parent_object_id')
    order = models.PositiveIntegerField()
    def __str__(self):
        return self.name
    

class OrderedItem(models.Model):
    """Abstract base class for items that need to be ordered within a container."""
    order = models.PositiveIntegerField(default=0, db_index=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True
        ordering = ['order']

class Option(models.Model):
    name = models.CharField(max_length=255)
    value = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    def __str__(self):
        return self.name