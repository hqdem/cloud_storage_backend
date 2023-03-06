from django.contrib.auth import get_user_model
from django.db import models


class File(models.Model):
    file = models.FileField(upload_to='files/%Y/%m/%d/', verbose_name='Файл')
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='files',
                              verbose_name='Пользователь')
    shared_users = models.ManyToManyField(get_user_model(), blank=True, related_name='sharing_files', verbose_name='Общие файлы')
    directory = models.ForeignKey('Directory', on_delete=models.CASCADE, blank=True, null=True, related_name='files', verbose_name='Директория')

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return self.file.name


class Directory(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    # files = models.ManyToManyField('File', blank=True, related_name='dirs', verbose_name='Файлы')
    parent_dir = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='children',
                                   verbose_name='Родительская директория')
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='dirs',
                              verbose_name='Пользователь')
    shared_users = models.ManyToManyField(get_user_model(), blank=True, related_name='sharing_dirs', verbose_name='Общие директории')

    class Meta:
        verbose_name = 'Папка'
        verbose_name_plural = 'Папки'

    def __str__(self):
        return self.name
