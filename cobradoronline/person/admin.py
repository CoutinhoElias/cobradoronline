from django.contrib import admin
from cobradoronline.person.models import Person, Movimento


# Register your models here.
# class PersonModelAdmin(admin.ModelAdmin):
#     pass
#     # inlines = [AdressInline]
#     list_display = ('pk',
#                     'name',
#                     'public_place',
#                     'number', 'city',
#                     'state',
#                     'zipcode',
#                     'neighborhood',
#                     'balance',
#                     'date_of_turn',
#                     'date_return')
#
#
# admin.site.register(Person, PersonModelAdmin)
class MyModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)


@admin.register(Person)
class PersonModelAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'user',
                    'name',
                    'public_place',
                    'number', 'city',
                    'state',
                    'zipcode',
                    'neighborhood',
                    'balance',
                    'date_of_turn',
                    'date_return')
    # exclude = ['user', ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        print(request.user, '<<<<<<<<<')
        # if request.user.is_superuser:
        #     return qs

        return qs.filter(user=(request.user, 2))

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Movimento)
class MovimentoModelAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'person', 'transaction_kind', 'value_moved', 'created',  'modified', 'date_return')
    exclude = ['user', ]

    # PERMITE QUE O FK SEJA LISTADO SOMENTE COM FILTROS PERSONALIZADOS
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "person":
            kwargs["queryset"] = Person.objects.filter(user_id=(request.user, 2))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
