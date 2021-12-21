# Generated by Django 4.0 on 2021-12-21 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0002_rubric_alter_bb_options_alter_bb_content_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bb',
            name='kind',
            field=models.CharField(blank=True, choices=[(None, 'Выберите тип публикуемого объявления'), ('b', 'Куплю'), ('s', 'Продам'), ('c', 'Обменяю')], max_length=1),
        ),
    ]