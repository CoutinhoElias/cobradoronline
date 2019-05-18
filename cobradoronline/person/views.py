import datetime

from django.db.models import Sum, Count
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, request
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.template.loader import get_template
from django import template

from django.utils.timezone import now
from datetime import datetime

from django.views.generic.dates import timezone_today

from cobradoronline.person.forms import PersonForm, MovimentoForm
from cobradoronline.person.models import Person, Movimento

from django.views.generic import View

from cobradoronline.utils import render_to_pdf


class GeneratePDF(View):
    def get(self, request, id, *args, **kwargs):
        template = get_template('recibo.html')

        person = Person.objects.get(id=id)
        movements = Movimento.objects.filter(person_id=id)

        context = {
            'person': person,
            'movements': movements
        }

        html = template.render(context)
        pdf = render_to_pdf('recibo.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


def person_create(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.user = request.user
            new.save()
            form.save_m2m()

            return HttpResponseRedirect('/cliente/lista/')
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            return render(request, 'person_create.html', {'form': form})
    else:
        context = {'form': PersonForm()}
        return render(request, 'person_create.html', context)


def person_return(request):
    q = request.GET.get('searchInput')

    if q:
        persons = Person.objects.filter(name__icontains=q, date_return__lte=now())
    else:
        persons = Person.objects.filter(date_return__lte=now())
    context = {'persons': persons}
    print(context)
    return render(request, 'person_return.html', context)


register = template.Library()


@register.simple_tag
def total_venda(request):
    q = request.GET.get('searchInput')
    if q:
        date_query = datetime.strptime(q, '%d/%m/%Y').date()
        return Movimento.objects.filter(created__contains=date_query,
                                        transaction_kind__icontains='out').aggregate(total=Sum('value_moved'))
    else:
        # date_query = now().year, now().month, now().day
        return Movimento.objects.filter(created__lt=timezone_today(),
                                        transaction_kind__icontains='out').aggregate(Sum('value_moved'))


def movement_accountability(request, i=0):
    q = request.GET.get('searchInput')
    if q:
        date_query = datetime.strptime(q, '%d/%m/%Y').date()

        # moviments = Movimento.objects.filter(created__contains=date_query)
        moviments = Movimento.objects.select_related().\
            filter(created__contains=date_query).\
            values('user__username', 'transaction_kind').annotate(Sum('value_moved'))

        saida = Movimento.objects.filter(created__contains=date_query,
                                         transaction_kind__icontains='out').aggregate(Sum('value_moved'))
        compra = Movimento.objects.filter(created__contains=date_query,
                                          transaction_kind__icontains='in').aggregate(Sum('value_moved'))

        moviments.total_venda = saida['value_moved__sum']
        moviments.total_compra = compra['value_moved__sum']

    else:
        moviments = Movimento.objects.select_related().\
            filter(created__contains=timezone_today()).\
            values('user__username', 'transaction_kind').annotate(Sum('value_moved'))

        saida = Movimento.objects.filter(created__contains=timezone_today(),
                                         transaction_kind__icontains='out').aggregate(Sum('value_moved'))
        compra = Movimento.objects.filter(created__contains=timezone_today(),
                                          transaction_kind__icontains='in').aggregate(Sum('value_moved'))

        moviments.total_venda = saida['value_moved__sum']
        moviments.total_compra = compra['value_moved__sum']

    context = {'moviments': moviments}
    return render(request, 'moviment_accountability.html', context)


def movement_accountability2(request, i=0):
    q = request.GET.get('searchInput')
    if q:
        date_query = datetime.strptime(q, '%d/%m/%Y').date()
        moviments = Movimento.objects.filter(created__contains=date_query)
        saida = Movimento.objects.\
            filter(created__contains=date_query, transaction_kind__icontains='out').aggregate(Sum('value_moved'))
        compra = Movimento.objects.\
            filter(created__contains=date_query, transaction_kind__icontains='in').aggregate(Sum('value_moved'))
        moviments.total_venda = saida['value_moved__sum']
        moviments.total_compra = compra['value_moved__sum']

        print(saida['value_moved__sum'])
    else:
        moviments = Movimento.objects.filter(created__contains=timezone_today())
        saida = Movimento.objects.\
            filter(created__contains=timezone_today(), transaction_kind__icontains='out').aggregate(Sum('value_moved'))
        compra = Movimento.objects.\
            filter(created__contains=timezone_today(), transaction_kind__icontains='in').aggregate(Sum('value_moved'))
        from django.db.models import Count

        moviments.total_venda = saida['value_moved__sum']
        moviments.total_compra = compra['value_moved__sum']

    context = {'moviments': moviments}
    return render(request, 'moviment_accountability.html', context)


def wall_copy(request):
    posts = Movimento.objects.values('person__name', 'transaction_kind').\
        annotate(Sum('value_moved'), Count('transaction_kind')).values()

    return JsonResponse(posts, safe=False)


def person_turn(request):
    q = request.GET.get('searchInput')

    if q:
        print(q)
        persons = Person.objects.filter(name__icontains=q, date_of_turn__lte=now())
    else:
        persons = Person.objects.filter(date_of_turn__lte=now())
    context = {'persons': persons}
    print(context)
    return render(request, 'person_turn.html', context)


def person_list(request):
    q = request.GET.get('searchInput')

    if q:
        print(q)
        persons = Person.objects.filter(name__icontains=q, user=request.user)
    else:
        persons = Person.objects.filter(user=request.user)
    context = {'persons': persons}
    print(context)
    return render(request, 'person_list.html', context)


def person_view(request, id):
    person = Person.objects.get(id=id)
    movements = Movimento.objects.filter(person_id=id)

    context = {
        'person':person,
        'movements':movements
    }
    return render(request, 'person_view.html', context)


def movement_create(request):

    user_id = request.user
    print(request.user)

    if request.method == 'POST':
        form = MovimentoForm(user_id, request.POST)

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.user = request.user
            new.save()
            form.save_m2m()

            return HttpResponseRedirect('/cliente/lista/')
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            print(form)
            return render(request, 'movement_create.html', {'form': form})
    else:
        # user_id no GET ta sendo passado para o forms.py, assim pego o id do usuario para meu queryset.
        context = {'form': MovimentoForm(user_id)}
        return render(request, 'movement_create.html', context)
