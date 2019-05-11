from django.contrib import admin
from cobradoronline.person.models import Person, Movimento


# Register your models here.
class PersonModelAdmin(admin.ModelAdmin):
    pass
    # inlines = [AdressInline]
    list_display = ('pk','name', 'public_place', 'number', 'city',  'state', 'zipcode', 'neighborhood', 'balance', 'date_of_turn','date_return')


admin.site.register(Person, PersonModelAdmin)


@admin.register(Movimento)
class MovimentoModelAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'person', 'transaction_kind', 'value_moved', 'created',  'modified', 'date_return')
    exclude = ['user', ]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)