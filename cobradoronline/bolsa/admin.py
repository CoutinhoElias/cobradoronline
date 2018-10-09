# Register your models here.
from cobradoronline.bolsa.models import PlanoDeContas, Questions, Pesquisa
from django.contrib import admin


class PlanoDeContasAdmin(admin.ModelAdmin):
    list_display = ['classification', 'name', 'reduced_account', 'sn', 'n', 'source', 'account_type']
    search_fields = ['classification', 'name', 'reduced_account', 'sn', 'n', 'source', 'account_type']


admin.site.register(PlanoDeContas, PlanoDeContasAdmin)


class QuestionsModelAdmin(admin.ModelAdmin):
    pass

admin.site.register(Questions, QuestionsModelAdmin)

class PesquisaModelAdmin(admin.ModelAdmin):
    pass

admin.site.register(Pesquisa, PesquisaModelAdmin)