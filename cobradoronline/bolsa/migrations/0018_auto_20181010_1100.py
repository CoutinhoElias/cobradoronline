# Generated by Django 2.0.7 on 2018-10-10 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0001_initial'),
        ('bolsa', '0017_auto_20181010_1059'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='pesquisa',
            unique_together={('search_key', 'person', 'question')},
        ),
    ]