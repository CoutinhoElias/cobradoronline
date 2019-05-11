# Generated by Django 2.0.7 on 2019-05-11 14:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('person', '0006_auto_20190511_1116'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pesquisa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_key', models.CharField(max_length=200, verbose_name='Chave da pesquisa')),
                ('response', models.CharField(choices=[('V', 'Verdadeiro'), ('F', 'Falso'), ('I', 'Indefinido')], default='I', max_length=1, verbose_name='Resposta')),
                ('participation_on', models.DateField(default=django.utils.timezone.now, verbose_name='período dapesquisa')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, verbose_name='solicitado em')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Pessoa', to='person.Person')),
            ],
            options={
                'verbose_name': 'Pesquisa',
                'verbose_name_plural': 'Pesquisas',
                'ordering': ('-participation_on',),
            },
        ),
        migrations.CreateModel(
            name='PlanoDeContas',
            fields=[
                ('classification', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='Classificação')),
                ('name', models.CharField(max_length=100, verbose_name='Descrição')),
                ('reduced_account', models.CharField(max_length=100, verbose_name='Conta reduzida')),
                ('sn', models.CharField(max_length=100, verbose_name='SN')),
                ('n', models.CharField(max_length=5, verbose_name='N')),
                ('source', models.CharField(max_length=100, verbose_name='Origem')),
                ('account_type', models.CharField(max_length=8, verbose_name='Tipo Conta')),
            ],
            options={
                'verbose_name': 'Plano de contas',
                'verbose_name_plural': 'Planos de conta',
                'ordering': ('classification',),
            },
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200, verbose_name='Pergunta')),
                ('level', models.CharField(choices=[('0', 'Indefinido'), ('1', 'Dependencia'), ('2', 'Confianca'), ('3', 'Comprometimento'), ('4', 'Preditiva'), ('5', 'Comprometimento')], default='0', max_length=15, verbose_name='Nível')),
            ],
            options={
                'verbose_name': 'Questão',
                'verbose_name_plural': 'Questões',
                'ordering': ('-level',),
            },
        ),
        migrations.AddField(
            model_name='pesquisa',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Pergunta', to='bolsa.Questions'),
        ),
        migrations.AlterUniqueTogether(
            name='pesquisa',
            unique_together={('search_key', 'person', 'question')},
        ),
    ]
