# Generated by Django 5.1.3 on 2024-12-05 08:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('products', '0001_initial'),
        ('store', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='category',
        ),
        migrations.RemoveField(
            model_name='store',
            name='product',
        ),
        migrations.AddField(
            model_name='store',
            name='categories',
            field=models.ManyToManyField(related_name='stores', to='categories.category'),
        ),
        migrations.AddField(
            model_name='store',
            name='products',
            field=models.ManyToManyField(related_name='stores', to='products.centralizedproduct'),
        ),
        migrations.AddField(
            model_name='store',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='stores/'),
        ),
        migrations.AlterField(
            model_name='store',
            name='owner',
            field=models.ForeignKey(limit_choices_to={'user_type__in': ['merchant', 'tasker']}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
