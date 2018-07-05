#from django import forms

import django_filters

from danibraz.bolsa.models import PlanoDeContas

class PlanoDeContasFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    #year_joined = django_filters.NumberFilter(name='date_joined', lookup_expr='year')
    #groups = django_filters.ModelMultipleChoiceFilter(queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = PlanoDeContas
        fields = ['name']
        #fields = ['username', 'first_name', 'last_name', 'year_joined', 'groups']