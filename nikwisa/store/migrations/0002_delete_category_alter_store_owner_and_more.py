# Generated by Django 5.1.4 on 2024-12-24 19:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.AlterField(
            model_name='store',
            name='owner',
            field=models.ForeignKey(limit_choices_to={'user_type__in': ['merchant', 'tasker']}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reaction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_reactions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='message',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='storereview',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_reviews', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='storeimage',
            name='store',
        ),
        migrations.RemoveField(
            model_name='offering',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='offering',
            name='price',
        ),
        migrations.RemoveField(
            model_name='offering',
            name='store',
        ),
        migrations.RemoveField(
            model_name='offering',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='offering',
            name='wedding_category',
        ),
        migrations.AddField(
            model_name='offering',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='offerings_images/'),
        ),
        migrations.AlterField(
            model_name='offering',
            name='description',
            field=models.TextField(default=5463728922763),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
        migrations.DeleteModel(
            name='StoreImage',
        ),
    ]