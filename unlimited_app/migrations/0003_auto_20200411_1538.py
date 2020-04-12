# Generated by Django 3.0.5 on 2020-04-11 10:08

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('unlimited_app', '0002_ai_and_txt'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ImageFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(null=True, upload_to='image_file/')),
            ],
        ),
        migrations.CreateModel(
            name='ImageStore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('image_title', models.CharField(blank=True, max_length=1000, null=True)),
                ('image_description', models.TextField()),
                ('image_upload_date', models.DateField(default=datetime.date.today)),
                ('file_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unlimited_app.FileType')),
            ],
        ),
        migrations.CreateModel(
            name='MainCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='image_store',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='image_store',
            name='image_category_type',
        ),
        migrations.RemoveField(
            model_name='image_store',
            name='sub_category_type',
        ),
        migrations.AlterUniqueTogether(
            name='sub_category_image',
            unique_together=None,
        ),
        migrations.AlterUniqueTogether(
            name='type_of_image',
            unique_together=None,
        ),
        migrations.DeleteModel(
            name='AI_and_Txt',
        ),
        migrations.DeleteModel(
            name='Image_store',
        ),
        migrations.DeleteModel(
            name='Sub_Category_Image',
        ),
        migrations.DeleteModel(
            name='Type_of_Image',
        ),
        migrations.AddField(
            model_name='imagestore',
            name='image_tag',
            field=models.ManyToManyField(to='unlimited_app.Tag'),
        ),
        migrations.AddField(
            model_name='imagestore',
            name='sub_category_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unlimited_app.SubCategory'),
        ),
        migrations.AddField(
            model_name='imagestore',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='imagefile',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unlimited_app.ImageStore'),
        ),
    ]
