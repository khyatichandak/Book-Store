# Generated by Django 2.2.5 on 2019-12-10 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_member_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='image',
        ),
    ]
