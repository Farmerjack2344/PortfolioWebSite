# Generated by Django 5.0.6 on 2024-09-24 19:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0012_remove_post_is_posted_alter_comments_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 24, 19, 43, 5, 847811, tzinfo=datetime.timezone.utc)),
        ),
    ]
