from django import forms

from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import User
#from material import Layout, Fieldset, Row, Span6

from cobradoronline.bookings.models import Booking


class BookingsForm(forms.ModelForm):
    allday = forms.BooleanField(label='Dia inteiro', required=False)
    title = forms.CharField(label='Titulo do agendamento', widget=forms.TextInput(attrs={'class': 'form-control'}))
    start = forms.DateTimeField(label='Inicia em...', widget=forms.TextInput(attrs={'class': 'form-control'}))
    end = forms.DateTimeField(label='Termina em...', widget=forms.TextInput(attrs={'class': 'form-control'}))
    #created_on = forms.DateTimeField(label='Criado em...')
    authorized = forms.BooleanField(label='Autorizado', required=False)
    editable = forms.BooleanField(label='Editavel', required=False)
    # ABAIXO, CHOICES NO FORMS VAI TER UMALISTAGEM NO TEMPLATE
    color = forms.ChoiceField(label='Cor', choices=(('blue', 'blue'),
                                                    ('red', 'red'),
                                                    ('green', 'green'),
                                                    ('black', 'black')), widget=forms.Select(attrs={'class': 'form-control select2-list'}))
    #form-control select2-list
    overlap = forms.BooleanField(label='Sobrepor?', required=False)
    holiday = forms.BooleanField(label='Feriado?', required=False)
    participants = forms.ModelMultipleChoiceField(label='Participantes', queryset=User.objects.all(), widget=FilteredSelectMultiple("Participantes", is_stacked=False, attrs={'id':'multi-select'}))

    class Meta:
        model = Booking
        exclude = ['created_on']
        fields = '__all__'

    # layout = Layout(
    #     Fieldset('Inclua uma agenda',
    #              Row('title', ),
    #              Row('start','end', 'color'),
    #              Row(Span6('holiday'),Span6('authorized'), ),
    #              Row(Span6('editable'), Span6('allday')),
    #              Row('overlap'),
    #              Row('participants')
    #              )
    # )