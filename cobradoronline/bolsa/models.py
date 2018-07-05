from django.db import models
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