from django import forms
from django.forms import ChoiceField

from cobradoronline.person.models import Person, Movimento
from django.contrib.admin.widgets import AdminTextInputWidget, FilteredSelectMultiple


#, default='Brasil', editable=False
class PersonForm(forms.ModelForm):
    name = forms.CharField(label='Nome', required=True, widget=AdminTextInputWidget(attrs={'class':'form-control input-lg'}))
    public_place = forms.CharField(label='Endereço completo', widget=AdminTextInputWidget(attrs={'class':'form-control input-lg'}))
    number = forms.CharField(label='Número', widget=AdminTextInputWidget(attrs={'class':'form-control input-lg'}))
    city = forms.CharField(label='Cidade', widget=AdminTextInputWidget(attrs={'class':'form-control input-lg'}))
    state = forms.CharField(label='Estado', widget=AdminTextInputWidget(attrs={'class':'form-control input-lg'}))
    zipcode = forms.CharField(label='Cep', widget=AdminTextInputWidget(attrs={'class':'form-control input-lg'}))
    neighborhood = forms.CharField(label='Bairro', widget=AdminTextInputWidget(attrs={'class':'form-control input-lg'}))
    balance = forms.DecimalField(label='Saldo', widget=AdminTextInputWidget(attrs={'class': 'form-control input-lg'}))
    #class="form-control input-lg"
    class Meta:
        model = Person
        fields = '__all__'


TRANSACTION_KIND = (
    ("---", "---------"),
    ("in", "Cliente Pagou"),
    ("out", "Cliente Recebeu"),
    ("eaj", "Ajuste pagamento do Cliente"),
    ("saj", "Ajuste recebimento do Cliente")
)


class MovimentoForm(forms.ModelForm):
    person = forms.ModelChoiceField(label='Pessoa', widget=forms.Select(attrs={'class': 'form-control'}), required=True, queryset=Person.objects.all())
    transaction_kind = forms.ChoiceField(label='Tipo Movimento', widget=forms.Select(attrs={'class': 'form-control'}), required=True, choices=TRANSACTION_KIND)
    value_moved = forms.DecimalField(label='Valor Movimentado', widget=AdminTextInputWidget(attrs={'class': 'form-control input-lg'}) , max_digits=10, decimal_places=2)

    class Meta:
        model = Movimento
        exclude = ['created','modified']
        fields = '__all__'
