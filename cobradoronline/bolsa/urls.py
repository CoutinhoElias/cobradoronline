from django.conf.urls import url, include
from django.views.i18n import JavaScriptCatalog

from cobradoronline.bolsa.views import planodecontas_list, simple_upload, planodecontas_export, addQuestions, questions

app_name = 'bolsa'

urlpatterns = [
    url(r'planodecontas/listar/$', planodecontas_list, name='planodecontas_list'),

    url(r'planodecontas/importar/$', simple_upload, name='simple_upload'),
    url(r'planodecontas/exportar/$', planodecontas_export, name='planodecontas_export'),

    url(r'pesquisa/criar/$', addQuestions, name='addQuestions'),
    url(r'pesquisa/listar/$', questions, name='questions'),

    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]