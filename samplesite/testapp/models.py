from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User

class Spare(models.Model):
    name = models.CharField(max_length=40, verbose_name='Деталь')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Детали'
        verbose_name = 'Деталь'


class Machine(models.Model):
    name = models.CharField(max_length=30, verbose_name='Машина')
    spares = models.ManyToManyField('Spare', verbose_name='Детали',
                                    through='Kit', through_fields=('machine', 'spare'))
    notes = GenericRelation('Note')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Машины'
        verbose_name = 'Машина'


class Kit(models.Model):
    machine = models.ForeignKey('Machine', on_delete=models.CASCADE, verbose_name='Машина')
    spare = models.ForeignKey('Spare', on_delete=models.CASCADE, verbose_name='Деталь')
    count = models.IntegerField(verbose_name='Количество')

    class Meta:
        verbose_name_plural = 'Количество деталей'
        verbose_name = 'Количество деталей'


# Пример модели с полиморфной связью
class Note(models.Model):
    content = models.TextField()
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type',
                                       fk_field='object_id')

    class Meta:
        verbose_name_plural = 'Заметки'
        verbose_name = 'Заметки'


# # Гл. 16.4.1 Пример прямого наследования моделей.
# class Message(models.Model):
#     content = models.TextField(default='')
#
#
# class PrivateMessage(Message):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     message = models.OneToOneField('Message', on_delete=models.CASCADE, parent_link=True)
#
#
# # Гл. 16.4.1 Пример Абстрактных моделей
# class Message(models.Model):
#     content = models.TextField(default='')
#     name = models.CharField(max_length=20)
#     email = models.EmailField()
#
#     class Meta:
#         abstract = True
#         ordering = ['name']
#
#
# class PrivateMessage(Message):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     message = models.OneToOneField('Message', on_delete=models.CASCADE, parent_link=True)
#     # Переопределяем поле name.
#     name = models.CharField(max_length=40)
#     # Удаляем поле email.
#     email = None
#
#     # Наследование поля name из класса Meta модели Message.
#     class Meta(Message.Meta):
#         pass

