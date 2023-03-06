# Generated by Django 4.1.7 on 2023-03-06 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_directory_shared_users_file_shared_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='directory',
            name='files',
        ),
        migrations.AddField(
            model_name='file',
            name='directory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='api.directory', verbose_name='Директория'),
        ),
    ]