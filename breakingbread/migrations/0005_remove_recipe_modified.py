# Generated by Django 2.1.5 on 2020-02-27 22:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('breakingbread', '0004_auto_20200226_1352'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='modified',
        ),
    ]
