import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template.loader import get_template

from django.utils.timezone import now
from datetime import datetime

from django.views.generic.dates import timezone_today

from cobradoronline.person.forms import PersonForm, MovimentoForm
from cobradoronline.person.models import Person, Movimento

from django.views.generic import View

from cobradoronline.utils import render_to_pdf #created in step 4
from django.utils.dateparse import parse_date

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
        print(q)
        persons = Person.objects.filter(name__icontains=q, date_return__lte=now())
    else:
        persons = Person.objects.filter(date_return__lte=now())
    context = {'persons': persons}
    print(context)
    return render(request, 'person_return.html', context)





def movement_accountability(request):
    q = request.GET.get('searchInput')
    if q:
        date_query = datetime.strptime(q, '%d/%m/%Y').date()
        print(date_query)
        persons = Movimento.objects.filter(created__contains=date_query)
    else:
        date_query = now().year, now().month, now().day
        persons = Movimento.objects.filter(created__contains=timezone_today())
    context = {'persons': persons}
    print(context)
    return render(request, 'person_accountability.html', context)


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