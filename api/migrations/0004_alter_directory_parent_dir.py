# Generated by Django 4.1.7 on 2023-02-27 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_directory_files'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directory',
            name='parent_dir',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='api.directory', verbose_name='Родительская директория'),
        ),
    ]
