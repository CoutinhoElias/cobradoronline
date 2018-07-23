from django.conf.urls import url, include
from django.views.i18n import JavaScriptCatalog

from cobradoronline.person.views import person_create, person_list, movement_create

app_name = 'person'

urlpatterns = [
    url(r'novo/$', person_create, name='person_create'),
    url(r'lista/$', person_list, name='person_list'),
    url(r'movimento/$', movement_create, name='movement_create'),

    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]