# Generated by Django 5.0.4 on 2024-06-25 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_blog'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='post',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
