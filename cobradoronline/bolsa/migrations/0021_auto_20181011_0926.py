# Generated by Django 2.0.7 on 2018-10-11 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bolsa', '0020_auto_20181010_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pesquisa',
            name='search_key',
            field=models.CharField(max_length=50, verbose_name='Chave da pesquisa'),
        ),
    ]
