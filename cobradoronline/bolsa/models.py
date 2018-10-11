from django.db import models
from django.utils import timezone
#DATA-PAPEL-OP(COMPRA.VENDA,DIVIDENDOS,SPLIT), QTD, CUSTO TOTAL(CORRETAGEM+IMPOSTOS)
# Create your models here.

#0.00.00.00.00.00.0000-0
class PlanoDeContas(models.Model):
    classification = models.CharField('Classificação', primary_key=True, max_length=100)
    name = models.CharField('Descrição', max_length=100)
    reduced_account = models.CharField('Conta reduzida', max_length=100)
    sn = models.CharField('SN', max_length=100)
    n = models.CharField('N', max_length=5)
    source = models.CharField('Origem', max_length=100)
    account_type = models.CharField('Tipo Conta', max_length=8)
    
    class Meta:
        verbose_name = 'Plano de contas'
        verbose_name_plural = 'Planos de conta'
        ordering = ('classification',)

    def __str__(self):
        return self.name


class Questions(models.Model):
    LEVEL_CHOICES = (
        ('0', 'Indefinido'),
        ('1', 'Dependencia'),
        ('2', 'Confianca'),
        ('3', 'Comprometimento'),
        ('4', 'Preditiva'),
        ('5', 'Comprometimento'),
    )
    question = models.CharField('Pergunta', max_length=200)
    level = models.CharField('Nível', max_length=15, choices=LEVEL_CHOICES, default='0')

    class Meta:
        verbose_name = 'Questão'
        verbose_name_plural = 'Questões'
        ordering = ('-level',)

    def __str__(self):
        return self.question

class PesquisaManager(models.Manager):
    def add_question(self, search_key, question):
        pesquisa, created = self.get_or_create(search_key=search_key, question=question)
        if not created:
            pesquisa.person = pesquisa.person
            pesquisa.question = pesquisa.question
            pesquisa.save()
        return pesquisa

class Pesquisa(models.Model):
    RESPOSTA_CHOICES = (
        ('V', 'Verdadeiro'),
        ('F', 'Falso'),
        ('I', 'Indefinido'),
    )
    search_key = models.CharField('Chave da pesquisa', max_length=50, db_index=False)
    person = models.ForeignKey('person.person', related_name='Pessoa', on_delete=models.CASCADE)
    question = models.ForeignKey('bolsa.Questions', related_name='Pergunta', on_delete=models.CASCADE,)
    response = models.CharField('Resposta', max_length=1, choices=RESPOSTA_CHOICES, default='I')
    participation_on = models.DateField('período dapesquisa', default=timezone.now)
    created_on = models.DateTimeField('solicitado em', default=timezone.now)

    objects = PesquisaManager()


    class Meta:
        verbose_name = 'Pesquisa'
        verbose_name_plural = 'Pesquisas'
        unique_together = (('search_key', 'person', 'question'),)
        ordering = ('-participation_on',)

    def __str__(self):
        return self.question.question

    # def get_absolute_url(self):
    #     return reverse('scheduling:agendamento')