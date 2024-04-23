# Generated by Django 5.0 on 2024-04-13 09:07

import apps.panel.utils
import django.core.files.storage
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/var/www/www-root/data/www/to-create.online/nails/media/files'), upload_to=apps.panel.utils.upload_to, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx'])]),
        ),
        migrations.AlterField(
            model_name='slice',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='icons/'),
        ),
        migrations.AlterField(
            model_name='slice',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
