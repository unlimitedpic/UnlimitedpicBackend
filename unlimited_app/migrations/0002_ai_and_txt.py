# Generated by Django 2.1 on 2019-11-17 04:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unlimited_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AI_and_Txt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ai_file', models.FileField(null=True, upload_to='Unlimited_images/ai_file/')),
                ('txt_file', models.FileField(null=True, upload_to='Unlimited_images/txt_file/')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='unlimited_app.Image_store')),
            ],
        ),
    ]