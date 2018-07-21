from django import forms
from cobradoronline.person.models import Person
from django.contrib.admin.widgets import AdminTextInputWidget

#, default='Brasil', editable=False
class PersonForm(forms.ModelForm):
    name = forms.CharField(label='Nome', required=True, widget=AdminTextInputWidget(attrs={'class':'form-control'}))
    public_place = forms.CharField(label='Endereço completo', widget=AdminTextInputWidget(attrs={'class':'form-control'}))
    number = forms.CharField(label='Número', widget=AdminTextInputWidget(attrs={'class':'form-control'}))
    city = forms.CharField(label='Cidade', widget=AdminTextInputWidget(attrs={'class':'form-control'}))
    state = forms.CharField(label='Estado', widget=AdminTextInputWidget(attrs={'class':'form-control'}))
    zipcode = forms.CharField(label='Cep', widget=AdminTextInputWidget(attrs={'class':'form-control'}))
    neighborhood = forms.CharField(label='Bairro', widget=AdminTextInputWidget(attrs={'class':'form-control'}))
    balance = forms.CharField(label='Saldo', widget=AdminTextInputWidget(attrs={'class': 'form-control'}))
    #class="form-control"
    class Meta:
        model = Person
        fields = '__all__'