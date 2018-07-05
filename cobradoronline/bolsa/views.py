# Create your views here.
from cobradoronline.bolsa.models import PlanoDeContas

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render

import xlrd


def simple_upload(request):
    if request.FILES:
        print(request.POST, 'POST')
        print(request.FILES, 'FILES')
        print(request.FILES['file'], 'FILES.file')

    if request.method == 'POST' and request.FILES['file']:
        myfile = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        #uploaded_file_url = fs.url(filename)
        filepath = fs.path(myfile.name)

        importaPlanilha(filepath)

        # return HttpResponseRedirect('/bolsa/planodecontas/listar/')
        # como é feito um ajax, não adianta o usar o redirect do django.
        # vc pode retornar um json como esse e chegar no JS se tudo ocorreu bem e assim
        # redirecionar com JS
        return JsonResponse({'statuss': 'success', 'names': 'vitor'})
    return render(request, 'import_form.html')

# def simple_upload(request):
#     if request.method == 'POST' and request.FILES:
#         myfile = request.FILES
#         fs = FileSystemStorage()
#         filename = fs.save(myfile, myfile)
#         #uploaded_file_url = fs.url(filename)
#         dir = fs.path(myfile)
#
#         importaPlanilha(dir)
#
#         return HttpResponseRedirect('/bolsa/planodecontas/listar/')
#
#     return render(request, 'import_form.html')

def remove(field):
    a = str(field)

    if a[len(a) - 2:] == '.0':
        a = a[:len(a) - 2]
    else:
        a = a.replace("-", "").replace(".", "")

    return a



def importaPlanilha(dir):
    #Funcionacom *.xls e *.xlsx

    workbook = xlrd.open_workbook(dir)
    #workbook = xlrd.open_workbook("/home/eliaspai/Área de Trabalho/MODELO_PLANO_DE_CONTAS_PARA_IMPORTAR.xlsx")

    # Posso usar sheet_by_name("Name") ou sheet_by_index(0, 1, 2, ..., N)
    #worksheet = workbook.sheet_by_name("Plan1")
    worksheet = workbook.sheet_by_index(0)

    lista = []

    #print(worksheet.nrows)
    for r in range(1, worksheet.nrows):
        lista.append(
            PlanoDeContas(classification=remove(str(worksheet.cell(r, 0).value)),
                          name=remove(str(worksheet.cell(r, 1).value)),
                          reduced_account=remove(str(worksheet.cell(r, 2).value)),
                          account_type=remove(str(worksheet.cell(r, 4).value)),
                          source=remove(str(worksheet.cell(r, 3).value)),

                          )
        )

    PlanoDeContas.objects.bulk_create(lista)
    return HttpResponseRedirect('/bolsa/planodecontas/listar/')


def planodecontas_list(request):
    q = request.GET.get('searchInput')
    print(request.GET)
    if q:
        print(q)
        planodecontas = PlanoDeContas.objects.filter(name__icontains=q)
    else:
        planodecontas = PlanoDeContas.objects.all()
    context = {'planodecontas': planodecontas}
    print(context)
    return render(request, 'bolsa_list.html', context)


def planodecontas_export(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="PlanoDeContas.txt"'

    planodecontas = PlanoDeContas.objects.all()

    #writer = response

    for planodecontas_obj in planodecontas:
        response.write(planodecontas_obj.classification + ' ' * (30 - len(planodecontas_obj.classification))
                   + ' ' * (30)
                   + planodecontas_obj.reduced_account + ' ' * (10 - len(planodecontas_obj.reduced_account))
                   + planodecontas_obj.account_type[:1]
                   + planodecontas_obj.name[:50] + ' ' * (50 - len(planodecontas_obj.name[:50]))
                   + planodecontas_obj.source[:1] + ' ' * (1 - len(planodecontas_obj.source[:1]))
                   + "INN"
                   + ' ' * (15)
                   + ' ' * (15)
                   + '0' * (10)
                   + "N"
                   + ' ' * (10)
                   + "NNN"
                   + ' ' * (50)
                   + ' ' * (15)
                   + "NN"
                   + '0' * (10)
                   + ' ' * (30)
                   + '0' * (10)
                   + ' ' * (12)
                   + ' ' * (10)
                   + ' ' * (30)
                   + ' ' * (30)
                   + ' ' * (20)
                   + "\n")

    return response