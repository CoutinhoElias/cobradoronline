from django import forms
from django.contrib.auth.models import User

from cobradoronline.person.models import Person, Movimento
from django.contrib.admin.widgets import AdminTextInputWidget


# default='Brasil', editable=False
class PersonForm(forms.ModelForm):
    name = forms.CharField(label='Nome', required=True, widget=AdminTextInputWidget(attrs={'class':'form-control input-lg'}))
    public_place = forms.CharField(label='Endereço completo', widget=AdminTextInputWidget(attrs={'class':'form-control input-lg'}))
    number = forms.CharField(label='Número', widget=AdminTextInputWidget(attrs={'class':'form-control input-lg'}))
    city = forms.CharField(label='Cidade', widget=AdminTextInputWidget(attrs={'class':'form-control input-lg'}))
    state = forms.CharField(label='Estado', widget=AdminTextInputWidget(attrs={'class':'form-control input-lg'}))
    zipcode = forms.CharField(label='Cep', widget=AdminTextInputWidget(attrs={'class':'form-control input-lg'}))
    neighborhood = forms.CharField(label='Bairro', widget=AdminTextInputWidget(attrs={'class':'form-control input-lg'}))
    balance = forms.DecimalField(label='Saldo', widget=AdminTextInputWidget(attrs={'class': 'form-control input-lg'}))
    date_of_turn = forms.DateField(label='Dt. Giro', widget=forms.TextInput(attrs={'class': 'form-control input-lg'}))
    date_return = forms.DateField(required=False)
    # class="form-control input-lg"

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.fields['balance'].localize = True
        self.fields['balance'].widget.is_localized = True

    def clean_name(self):
        name = self.cleaned_data['name']
        return name.upper()

    class Meta:
        model = Person
        exclude = ['date_return', 'user']
        fields = '__all__'
        ordering = ('name',)


TRANSACTION_KIND = (
    ("---", "---------"),
    ("in", "Cliente Pagou"),
    ("out", "Cliente Recebeu"),
    ("eaj", "Ajuste pagamento do Cliente"),
    ("saj", "Ajuste recebimento do Cliente")
)


class MovimentoForm(forms.ModelForm):
    person = forms.ModelChoiceField(label='Pessoa', widget=forms.Select(attrs={'class': 'form-control'}), required=True,
                                    queryset=Person.objects.all())

    transaction_kind = forms.ChoiceField(label='Tipo Movimento',
                                         widget=forms.Select(attrs={'class': 'form-control'}),
                                         required=True, choices=TRANSACTION_KIND)
    value_moved = forms.DecimalField(label='Valor Movimentado',
                                     widget=AdminTextInputWidget(attrs={'class': 'form-control input-lg'}),
                                     max_digits=10,
                                     decimal_places=2)
    created = forms.DateField(label='Dt. Movimento',
                              widget=forms.TextInput(attrs={'class': 'form-control input-lg'}))
    date_return = forms.DateField(label='Dt. Retorno',
                                  widget=forms.TextInput(attrs={'class': 'form-control input-lg'}))

    # def __init__(self, user,  *args, **kwargs):
    #     super(MovimentoForm, self).__init__(*args, **kwargs)
    #     self.fields['moved'].widget.is_localized = True

    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)

        print(user_id)

        # user_id ta sendo passado via GET da VIEW, assim pego o id do usuario para meu queryset.
        self.fields['person'].queryset = Person.objects.filter(user_id=user_id)

        self.fields['value_moved'].localize = True
        self.fields['value_moved'].widget.is_localized = True

        """
        A variavel pk acima vem da view atendimento_create(request, pk): onde envio esse valor
        no GET na linha 29
        context = {'form': AtendimentoForm(pk)}
        """

    class Meta:
        model = Movimento
        exclude = ['modified', 'user']
        fields = '__all__'
        # ordering = ('person',)
