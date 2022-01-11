from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


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


class Note(models.Model):
    content = models.TextField()
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type',
                                       fk_field='object_id')
