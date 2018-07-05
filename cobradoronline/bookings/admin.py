from django.contrib import admin
from cobradoronline.bookings.models import Booking


class BookingModelAdmin(admin.ModelAdmin):
    pass

admin.site.register(Booking, BookingModelAdmin)
