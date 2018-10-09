import datetime

from django.db.models import Sum, Count
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, request
from django.shortcuts import render


# Create your views here.
from django.template.loader import get_template
from django import template

from django.utils.timezone import now
from datetime import datetime

from django.views.generic.dates import timezone_today
from rest_framework.response import Response

from cobradoronline.person.forms import PersonForm, MovimentoForm
from cobradoronline.person.models import Person, Movimento

from django.views.generic import View

from cobradoronline.utils import render_to_pdf

# class ChartData(View):
#     authentication_classes = []
#     permission_classes = []
#
#     def get(self, request, format=None):
#         qs_count = Movimento.objects.values('person__name','transaction_kind').annotate(arroz=Sum('value_moved'))
#         labels = ["qs_count", "Blue", "Yellow", "Green", "Purple", "Orange"]
#         print(qs_count)
#         default_items = [qs_count, 5, 6,4,3,9]
#         data = {
#             "labels": labels,
#             "default":default_items,
#             #"users": Movimento.objects.values('person__name','transaction_kind').annotate(arroz=Sum('value_moved'))
#         }
#
#         return Response(data)
# #-----------------------------------------------------------------------------------------------------------------------
# def get_data(request, *args, **kwargs):
#     data = Movimento.objects.values('person__name','transaction_kind').annotate(arroz=Sum('value_moved'))
#     return Response(data)

#-----------------------------------------------------------------------------------------------------------------------
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
            new.save()
            form.save_m2m()

            return HttpResponseRedirect('/cliente/lista/')
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            print(form)
            return render(request, 'person_create.html', {'form':form})
    else:
        context = {'form': PersonForm()}
        return render(request, 'person_create.html', context)


def person_return(request):
    q = request.GET.get('searchInput')
    #print(request.GET)
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
        return Movimento.objects.filter(created__contains=date_query, transaction_kind__icontains='out').aggregate(total=Sum('value_moved'))
    else:
        #date_query = now().year, now().month, now().day
        return Movimento.objects.filter(created__lt=timezone_today(), transaction_kind__icontains='out').aggregate(Sum('value_moved'))


def movement_accountability(request, i=0):
    q = request.GET.get('searchInput')
    if q:
        date_query = datetime.strptime(q, '%d/%m/%Y').date()
        moviments = Movimento.objects.filter(created__contains=date_query)
        saida = Movimento.objects.filter(created__contains=date_query, transaction_kind__icontains='out').aggregate(Sum('value_moved'))
        compra = Movimento.objects.filter(created__contains=date_query, transaction_kind__icontains='in').aggregate(Sum('value_moved'))
        moviments.total_venda = saida['value_moved__sum']
        moviments.total_compra = compra['value_moved__sum']

        print(saida['value_moved__sum'])
    else:
        import json
        #date_query = now().year, now().month, now().day
        moviments = Movimento.objects.filter(created__contains=timezone_today())
        saida = Movimento.objects.filter(created__contains=timezone_today(), transaction_kind__icontains='out').aggregate(Sum('value_moved'))
        compra = Movimento.objects.filter(created__contains=timezone_today(), transaction_kind__icontains='in').aggregate(Sum('value_moved'))
        from django.db.models import Count
        #testes = Movimento.objects.values('person__name','transaction_kind').aggregate(Sum('value_moved'), Count('transaction_kind'))
        testes = Movimento.objects.values('person__name','transaction_kind').annotate(Sum('value_moved'), Count('transaction_kind'))


        # for teste in testes:
        #     print(testes[i])
        #     i+= 1
        #
        # print('------------------------------------------------------------------------------')
        # print(testes)
        # print('------------------------------------------------------------------------------')
        moviments.total_venda = saida['value_moved__sum']
        moviments.total_compra = compra['value_moved__sum']



        # somatorios = {}
        #
        # for moviment in moviments:
        #     somatorio = somatorios.get(moviment.value_moved, 0)
        #     if moviment.transaction_kind == 'in' or moviment.transaction_kind == 'eaj':
        #         somatorio += moviment.value_moved
        #     else:
        #         somatorio -= moviment.value_moved
        #
        #     moviment.saldo = somatorio
        #     somatorios[moviment.value_moved] = somatorio

    context = {'moviments': moviments}
    return render(request, 'moviment_accountability.html', context)


def wall_copy(request):
    posts = Movimento.objects.values('person__name','transaction_kind').annotate(Sum('value_moved'), Count('transaction_kind')).values()

    return JsonResponse(posts, safe=False)

def person_turn(request):
    q = request.GET.get('searchInput')
    #print(request.GET)
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
    #print(request.GET)
    if q:
        print(q)
        persons = Person.objects.filter(name__icontains=q)
    else:
        persons = Person.objects.all()
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
    if request.method == 'POST':
        form = MovimentoForm(request.POST)

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.save()
            form.save_m2m()

            return HttpResponseRedirect('/cliente/lista/')
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            print(form)
            return render(request, 'movement_create.html', {'form':form})
    else:
        context = {'form': MovimentoForm()}
        return render(request, 'movement_create.html', context)