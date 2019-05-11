# Create your views here.
from django.views.generic import TemplateView

from cobradoronline.bolsa.models import PlanoDeContas

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render

from django.forms import modelformset_factory

import xlrd

from cobradoronline.person.models import Person


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


# def addQuestions(dir):
#     person = Person.objects.get(pk=1)
#     questions = Questions.objects.all()
#
#
#     print(person)
#
#     lista = []
#
#     for question in questions:
#         lista.append(
#             Pesquisa(search_key='092018',
#                           person=person,
#                           question=question,
#                           response='I'
#                           )
#         )
#
#     Pesquisa.objects.bulk_create(lista)
#     return HttpResponseRedirect('/admin/bolsa/pesquisa/')

# def pp(request):
#     if request.method == 'POST':
#         form = ProfissoesPessoaForm(request.POST)
#
#         if not form.is_valid():
#             return render(request, 'sosmypc/profissoes_pessoa_forms.html', {'form': form})
#
#         pessoa = request.POST['pessoa']
#         profissao = request.POST['profissao']
#         rating = request.POST['rating']
#
#         ProfissoesPessoa.objects.create(pessoa=pessoa.user.pessoa,
#                                         profissao=profissao,
#                                         rating=rating)
#
#         return HttpResponseRedirect('/cadastrarprofissaopessoa/')
#     else:
#         return render(request, 'sosmypc/profissoes_pessoa_forms.html',
#                       {'form': ProfissoesPessoaForm(initial={'pessoa': request.user.pessoa})})


def addQuestions(request):
    person = Person.objects.get(pk=1)
    questions = Questions.objects.all()

    for question in questions:
        try:
            Pesquisa.objects.get(
                search_key='092018',
                person=person,
                question=question
            )
            print('existe')
        except Pesquisa.DoesNotExist:
            Pesquisa.objects.get_or_create(
                search_key='092018',
                person=person,
                question=question,
                response='I'
            )
            print('Não existe')

    return HttpResponseRedirect('bolsa/pesquisa/listar')


class QuestionsDetailWiew(TemplateView):
    template_name = 'queryes.html'

    def get_formset(self, clear=False):
        QuestionsFormSet = modelformset_factory(
            Pesquisa, fields=('response',), can_delete=False, extra=0
        )
        if clear:
            formset = QuestionsFormSet(
                queryset = Pesquisa.objects.filter(search_key='092018')
            )
        else:
            formset = QuestionsFormSet(
                queryset = Pesquisa.objects.filter(search_key='092018'),
                data=self.request.POST or None
            )

        return formset

    def get_context_data(self, **kwargs):
        context = super(QuestionsDetailWiew, self).get_context_data(**kwargs)
        context['formset'] = self.get_formset()
        return context

    def post(self, request, *args, **kwargs):
        formset = self.get_formset()
        context = self.get_context_data(**kwargs)
        if formset.is_valid():
            print('Formulário válido!')
            formset.save()
            print('Dados salvos!')
            context['formset'] = self.get_formset(clear=True)
        else:
            print(formset)
        return self.render_to_response(context)


questions = QuestionsDetailWiew.as_view()


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
