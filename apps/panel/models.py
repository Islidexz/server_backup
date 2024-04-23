from mptt.models import MPTTModel, TreeForeignKey, TreeManager
from tinymce.models import HTMLField
#tree view
from config.base import *
#####
from django.conf import settings
from django.db import models
###
from mptt.templatetags.mptt_tags import *
from apps.panel.page_manager import *
from .utils import *
from django.core.validators import FileExtensionValidator


class Website(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='websites', # related_name is for the reverse relation
        verbose_name='Website Owner', null=True, blank=True # verbose_name is for the admin panel
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    url = models.URLField(unique=True, null=True, blank=True)
    state = models.CharField(
        max_length=10,
        choices=(('active', 'Active'), ('inactive', 'Inactive')),
        default='active'
    )
    type = models.CharField(
        max_length=10,
        choices=(('personal', 'Personal'), ('business', 'Business')),
        default='personal'
    )
    def __str__(self):
        return self.name or "Unnamed Website"
    

class Page(MPTTModel):
#class Page(TreebeardMPTTModel): 
    objects = PageManager()
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, default='Untitled', null=True, blank=True)
    text = HTMLField(blank=True, null=True)
    url = models.CharField(max_length=255, unique=True, null=True, blank=True, default='new-page')
    parent_ws = models.ForeignKey(Website, on_delete=models.SET_NULL, null=True, related_name='pages', default=1)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children') # as parent_id in django
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default='active')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='cat')

    def get_siblings(self, include_self=False):
        if not self.parent:
            return Page.objects.none()
        siblings = self.parent.get_children()
        if not include_self:
            siblings = siblings.exclude(id=self.id)
        return siblings

    class MPTTMeta:
        order_insertion_by = ['lft']
    def __str__(self):
        return self.title or None
        
    class Meta:
        unique_together = (('url', 'parent_ws'), ('url', 'parent'))
        indexes = [models.Index(fields=['url', 'parent'])]

class Slice(models.Model):
    id = models.AutoField(primary_key=True)
    parent_page = models.ForeignKey('Page', on_delete=models.SET_NULL, related_name='slices', null=True, blank=True)
    is_main = models.BooleanField(default=False)#
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default='active')
    price = models.FloatField(blank=True, null=True)
    title = models.CharField(max_length=255)
    text = HTMLField(blank=True, null=True)  # Changed from models.TextField to HTMLField
    timestamp = models.DateTimeField(auto_now_add=True)
    keywords_block = models.TextField(blank=True, null=True)# redo
    # New image fields
    icon = models.ImageField(upload_to='icons/', blank=True, null=True)
    img = models.ImageField(upload_to='images/', blank=True, null=True)
                                     ######
    file_validator = FileExtensionValidator(
        allowed_extensions = ALLOWED_IMAGE_FORMATS
    )
    class MPTTMeta:
        order_insertion_by = ['lft']
                                  ######
    #def __str__(self):
    #    return f'Slice for {self.parent_page}'
    def __str__(self):
        return self.title
                                  ######
    def save(self, *args, **kwargs):
        if self.file.name.endswith('.svg'):
            self.file = process_svg(self.file, 'file')
        super().save(*args, **kwargs)


from apps.panel.model_extra_classes import *