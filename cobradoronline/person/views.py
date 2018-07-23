from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from cobradoronline.person.forms import PersonForm, MovimentoForm
from cobradoronline.person.models import Person


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
    
    
def person_list(request):
    q = request.GET.get('searchInput')
    print(request.GET)
    if q:
        print(q)
        persons = Person.objects.filter(name__icontains=q)
    else:
        persons = Person.objects.all()
    context = {'persons': persons}
    print(context)
    return render(request, 'person_list.html', context)


# def clients_edit(request, person_id):
#     pessoa = get_object_or_404(Person, pk=person_id)
#     if request.method == 'POST':
#         form = PersonForm(request.POST, instance=pessoa)
#         movimentoform = MovimentoForm(request.POST, instance=pessoa)
#
#         if form.is_valid():
#             print('<<<<==== FORM VALIDO ====>>>>')
#             new = form.save(commit=False)
#             new.save()
#             form.save_m2m()
#             return HttpResponseRedirect('/cadastro/clientes/editar/'+person_id, person_id)
#         else:
#             print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
#             print(form)
#             return render(request, 'persons/person.html', {'form':form})
#     else:
#         print('Entrou em modo de edição do cliente '+person_id)
#
#         request.session['person_id'] = person_id
#         print('A variável person_id da session já possui o valor: '+request.session['person_id'])
#
#         person_instance = Person.objects.get(pk=request.session["person_id"])
#         initial_data = {"person": person_instance}
#
#         context = {'form': PersonForm(instance=pessoa), 'movimentoform': MovimentoForm(initial=initial_data)}
#         return render(request, 'persons/person_addresses.html', context)


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