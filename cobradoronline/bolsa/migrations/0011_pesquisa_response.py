# Generated by Django 2.0.7 on 2018-10-04 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bolsa', '0010_auto_20181004_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='pesquisa',
            name='response',
            field=models.CharField(choices=[('V', 'Verdadeiro'), ('F', 'Falso'), ('I', 'Indefinido')], default='I', max_length=1, verbose_name='Resposta'),
        ),
    ]
