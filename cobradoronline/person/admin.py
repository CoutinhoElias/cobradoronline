from django.contrib import admin
from cobradoronline.person.models import Person


# Register your models here.
class PersonModelAdmin(admin.ModelAdmin):
    pass
    #inlines = [AdressInline]
    list_display = ('pk','name', 'public_place', 'number', 'city',  'state', 'zipcode', 'country', 'neighborhood')

admin.site.register(Person, PersonModelAdmin)