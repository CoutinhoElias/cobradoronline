""" cobradoronline URL Configuration """

from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^bolsa/', include('cobradoronline.bolsa.urls', namespace='cobradoronline-bolsa')),
    url(r'^bookings/', include('cobradoronline.bookings.urls', namespace='cobradoronline-bookings')),
    url(r'^api/bookings/', include('cobradoronline.bookings.api.urls', namespace='booking-api')),
    path('admin/', admin.site.urls),
]
