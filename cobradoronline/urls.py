""" cobradoronline URL Configuration """

from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    #cob    url(r'^foo/', include('foo.urls', namespace='foo')),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^bolsa/', include('cobradoronline.bolsa.urls', namespace='bolsa')),
    url(r'^cliente/', include('cobradoronline.person.urls', namespace='person')),
    url(r'^bookings/', include('cobradoronline.bookings.urls', namespace='bookings')),
    url(r'^api/bookings/', include('cobradoronline.bookings.api.urls', namespace='booking-api')),
    path('admin/', admin.site.urls),
]
