# Generated by Django 5.1.4 on 2024-12-24 21:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
        ('store', '0001_initial'),
        ('weddings', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='offering',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offerings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reaction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_reactions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='store',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='stores', to='categories.category'),
        ),
        migrations.AddField(
            model_name='store',
            name='owner',
            field=models.ForeignKey(limit_choices_to={'user_type__in': ['merchant', 'tasker']}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='store',
            name='wedding_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='store_wedding_offerings', to='weddings.weddingscategory'),
        ),
        migrations.AddField(
            model_name='reaction',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='store.store'),
        ),
        migrations.AddField(
            model_name='offering',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offerings', to='store.store'),
        ),
        migrations.AddField(
            model_name='like',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.store'),
        ),
        migrations.AddField(
            model_name='storereview',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='store.store'),
        ),
        migrations.AddField(
            model_name='storereview',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_reviews', to=settings.AUTH_USER_MODEL),
        ),
    ]
