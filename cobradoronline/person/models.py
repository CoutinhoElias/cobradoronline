from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField('Nome',max_length=100)
    public_place = models.CharField('Logradouro',max_length=150)
    number = models.CharField('Número',max_length=150)
    city = models.CharField('Cidade',max_length=150)
    state = models.CharField('Estado',max_length=150)
    zipcode = models.CharField('Cep',max_length=10)
    neighborhood = models.CharField('Bairro',max_length=50)


    class Meta:
        verbose_name_plural = 'pessoas'
        verbose_name = 'pessoa'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return 'cliente/novo'