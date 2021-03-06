from django.conf.urls import url, include
from django.views.i18n import JavaScriptCatalog

from cobradoronline.person.views import person_create, person_list, movement_create, person_view, person_turn, \
    person_return, GeneratePDF, movement_accountability, wall_copy

app_name = 'person'


urlpatterns = [
    url(r'novo/$', person_create, name='person_create'),
    url(r'consultar/(?P<id>\d+)/$', person_view, name='person_view'),
    url(r'prestacao-de-contas/$', movement_accountability, name='movement_accountability'),
    url(r'json-dump/$', wall_copy, name='wall_copy'),
    # url(r'api/data/$', get_data, name='api-data'),

    #url(r'recibo/$', generatePdf, name='generatepdf'),

    url(r'recibo/(?P<id>\d+)/$', GeneratePDF.as_view(), name='generatepdf'),
    url(r'lista/$', person_list, name='person_list'),
    url(r'giro/$', person_turn, name='person_turn'),
    url(r'retorno/$', person_return, name='person_return'),
    url(r'movimento/$', movement_create, name='movement_create'),

    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]