# Generated by Django 4.1.7 on 2023-02-27 15:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='files', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Directory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название')),
                ('files', models.ManyToManyField(related_name='dirs', to='api.file', verbose_name='Файлы')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dirs', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('parent_dir', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to='api.directory', verbose_name='Родительская директория')),
            ],
            options={
                'verbose_name': 'Папка',
                'verbose_name_plural': 'Папки',
            },
        ),
    ]
