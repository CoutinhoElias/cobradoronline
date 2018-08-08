import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.utils.timezone import now

from cobradoronline.person.forms import PersonForm, MovimentoForm
from cobradoronline.person.models import Person, Movimento

from django.http import HttpResponse
from django.views.generic import View

from cobradoronline.utils import render_to_pdf #created in step 4

class generatePdf(View):
    def get(self, request, *args, **kwargs):
        data = {
            'today': datetime.date.today(),
            'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
        }
        print('Passou em generatePdf')
        pdf = render_to_pdf('recibo.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


# class GeneratePDF(View):
#     def get(self, request, *args, **kwargs):
#         template = get_template('recibo.html')
#         context = {
#             "invoice_id": 123,
#             "customer_name": "John Cooper",
#             "amount": 1399.99,
#             "today": "Today",
#         }
#         html = template.render(context)
#         pdf = render_to_pdf('recibo.html', context)
#         if pdf:
#             response = HttpResponse(pdf, content_type='application/pdf')
#             filename = "Invoice_%s.pdf" %("12341231")
#             content = "inline; filename='%s'" %(filename)
#             download = request.GET.get("download")
#             if download:
#                 content = "attachment; filename='%s'" %(filename)
#             response['Content-Disposition'] = content
#             return response
#         return HttpResponse("Not found")


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