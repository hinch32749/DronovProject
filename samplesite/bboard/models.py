from django.db import models


class Bb(models.Model):
    KINDS = (
        (None, 'Выберите тип публикуемого объявления'),
        ('b', 'Куплю'),
        ('s', 'Продам'),
        ('c', 'Обменяю'),
    )

    title = models.CharField(max_length=50, verbose_name='Товар')
    content = models.TextField(null=True, blank=True,
                               verbose_name='Описание')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    published = models.DateTimeField(auto_now_add=True, db_index=True,
                                     verbose_name='Опубликовано')
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT,
                               verbose_name='Рубрика')
    kind = models.CharField(max_length=1, choices=KINDS, blank=True,
                            verbose_name='Тип объявления')

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-published']

    def __str__(self):
        return self.title


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True,
                            verbose_name='Название')

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['name']

    def get_absolute_url(self):
        return '/bboard/%s/' % self.pk

    def __str__(self):
        return self.name