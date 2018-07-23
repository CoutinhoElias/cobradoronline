from django.db import models


TRANSACTION_KIND = (
    ("in", "Cliente Pagou"),
    ("out", "Cliente Recebeu"),
    ("eaj", "Ajuste pagamento do Cliente"),
    ("saj", "Ajuste recebimento do Cliente")
)

# Create your models here.
class Person(models.Model):
    name = models.CharField('Nome',max_length=100)
    balance = models.DecimalField('Saldo', max_digits=10, decimal_places=2)
    public_place = models.CharField('Logradouro',max_length=150)
    number = models.CharField('Número',max_length=150)
    city = models.CharField('Cidade',max_length=150)
    state = models.CharField('Estado',max_length=150)
    zipcode = models.CharField('Cep',max_length=10)
    neighborhood = models.CharField('Bairro',max_length=50)


    class Meta:
        verbose_name_plural = 'Pessoas'
        verbose_name = 'Pessoa'

    def stock_avaliable(self):
        itens_nota = Movimento.objects.select_related('person').all().order_by("created")
        total_avaliable = 0

        for transaction in itens_nota:
            if transaction.person.transaction_kind == 'in' or transaction.person.transaction_kind == 'eaj':
                total_avaliable += transaction.balance
            else:
                total_avaliable -= transaction.balance

        return total_avaliable

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return 'cliente/novo/'
    #
    # def get_absolute_url(self):
    #     return reverse('persons:person_edit', args=[str(self.id)])


class Movimento(models.Model):
    person = models.ForeignKey('person.Person', related_name='person_item',on_delete=models.CASCADE)
    transaction_kind = models.CharField('Tipo Movimento', max_length=4, choices=TRANSACTION_KIND)
    value_moved = models.DecimalField('Valor Movimento', max_digits=10, decimal_places=2)
    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField('modified', auto_now=True)

    class Meta:
        verbose_name = 'Movimento'
        verbose_name_plural = 'Movimentos'

def post_save_movimento(sender, instance, created,  **kwargs):
    if created:
        if instance.transaction_kind == 'in' or instance.transaction_kind == 'eaj':
            instance.person.balance += instance.value_moved
            instance.person.save()
        else:
            instance.person.balance -= instance.value_moved
            instance.person.save()
    else:
        instance.person.balance -= instance.person.balance
        instance.person.balance += instance.person.stock_avaliable()
        instance.person.save()

models.signals.post_save.connect(
    post_save_movimento, sender=Movimento, dispatch_uid='post_save_movimento'
)
