# Generated by Django 2.1.5 on 2020-03-12 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('breakingbread', '0006_auto_20200311_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='average_rating',
            field=models.IntegerField(default=0),
        ),
    ]