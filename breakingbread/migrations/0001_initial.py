# Generated by Django 2.1.5 on 2020-02-22 22:39

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('recipe_id', models.AutoField(primary_key=True, serialize=False)),
                ('recipe_name', models.CharField(max_length=128)),
                ('time_taken', models.IntegerField()),
                ('level', models.IntegerField()),
                ('ingredients', models.TextField(max_length=500)),
                ('cooking_type', models.IntegerField(default=0)),
                ('cuisine', models.CharField(max_length=128)),
                ('image1', models.ImageField(upload_to='recipe_images')),
                ('image2', models.ImageField(blank=True, upload_to='recipe_images')),
                ('image3', models.ImageField(blank=True, upload_to='recipe_images')),
                ('image4', models.ImageField(blank=True, upload_to='recipe_images')),
                ('image5', models.ImageField(blank=True, upload_to='recipe_images')),
                ('description', models.TextField(max_length=2000)),
                ('created', models.DateTimeField(default=datetime.datetime(2020, 2, 22, 22, 39, 15, 463300, tzinfo=utc))),
                ('modified', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('report_id', models.AutoField(primary_key=True, serialize=False)),
                ('post_type', models.IntegerField()),
                ('post_id', models.IntegerField()),
                ('description', models.TextField(max_length=500)),
                ('status', models.BooleanField(default=False)),
                ('action_taken', models.CharField(blank=True, max_length=500)),
                ('created', models.DateTimeField(default=datetime.datetime(2020, 2, 22, 22, 39, 15, 478920, tzinfo=utc))),
                ('modified', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('review_id', models.AutoField(primary_key=True, serialize=False)),
                ('rating', models.IntegerField(default=0)),
                ('description', models.TextField(max_length=500)),
                ('created', models.DateTimeField(default=datetime.datetime(2020, 2, 22, 22, 39, 15, 463300, tzinfo=utc))),
                ('recipe_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='breakingbread.Recipe')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usertype', models.IntegerField(default=0)),
                ('address', models.CharField(blank=True, max_length=300)),
                ('picture', models.ImageField(blank=True, upload_to='profile_images')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='review',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='breakingbread.UserProfile'),
        ),
        migrations.AddField(
            model_name='report',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='breakingbread.UserProfile'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='breakingbread.UserProfile'),
        ),
    ]
