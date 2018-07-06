from django import forms
from cobradoronline.person.models import Person

class PersonForm(forms.ModelForm):
    name = forms.CharField(label='Nome', required=True)
    purchase_limit = forms.DecimalField(label='Limite de compra')
    public_place = forms.CharField(label='Endereço completo')
    number = forms.CharField(label='Número')
    city = forms.CharField(label='Cidade')
    state = forms.CharField(label='Estado')
    zipcode = forms.CharField(label='Cep')
    country = forms.CharField(label='País')
    neighborhood = forms.CharField(label='Bairro')

    class Meta:
        model = Person
        fields = '__all__'