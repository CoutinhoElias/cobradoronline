from django.contrib import admin
from cobradoronline.person.models import Person, Movimento


# Register your models here.
class PersonModelAdmin(admin.ModelAdmin):
    pass
    #inlines = [AdressInline]
    list_display = ('pk','name', 'public_place', 'number', 'city',  'state', 'zipcode', 'neighborhood', 'balance')

admin.site.register(Person, PersonModelAdmin)

class MovimentoModelAdmin(admin.ModelAdmin):
    pass
    #inlines = [AdressInline]
    list_display = ('pk','person', 'transaction_kind', 'value_moved', 'created',  'modified')

admin.site.register(Movimento, MovimentoModelAdmin)