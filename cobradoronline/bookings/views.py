from datetime import date

from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from rest_framework.viewsets import ModelViewSet

from cobradoronline import bookings
from cobradoronline.bookings.forms import BookingsForm
from cobradoronline.bookings.models import Booking
from cobradoronline.bookings.serializer import BookingSerializer

class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


def bookings_list(request):
    selected_date = date.today()
    return list_date(request) #return list_date(request, selected_date.year, selected_date.month)


def list_date(request):
    return render(request, 'bookings/bookings_list.html') #def list_date(request, year, month):

# def bookings_create(request):
# 	if request.method == 'POST':
# 		form = BookingsForm(request.POST)
# 	else:
# 		form = BookingsForm()
# 	return save_all(request,form,'book_create.html')


def save_bookings_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            bookings = Booking.objects.all()
            data['html_book_list'] = render_to_string('bookings/includes/partial_bookings_list.html', {
                'books': bookings
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def bookings_create(request):
    if request.method == 'POST':
        form = BookingsForm(request.POST)
    else:
        form = BookingsForm()
    return save_bookings_form(request, form, 'bookings/includes/partial_book_create.html')


def bookings_update(request, pk):
    bookings = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        form = BookingsForm(request.POST, instance=bookings)
    else:
        form = BookingsForm(instance=bookings)
    return save_bookings_form(request, form, 'bookings/includes/partial_book_update.html')


def book_delete(request, pk):
    book = get_object_or_404(Booking, pk=pk)
    data = dict()
    if request.method == 'POST':
        bookings.delete()
        data['form_is_valid'] = True
        books = Booking.objects.all()
        data['html_bookings_list'] = render_to_string('bookings/includes/partial_book_list.html', {
            'bookings': books
        })
    else:
        context = {'bookings': bookings}
        data['html_form'] = render_to_string('bookings/includes/partial_book_delete.html', context, request=request)
    return JsonResponse(data)


#-----------------------------------------------------------------------------------------------------
def bookings_create1(request):
    data = dict()

    if request.method == 'POST':
        form = BookingsForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = BookingsForm()
    context = {'form': form}
    data['html_form'] = render_to_string('bookings_create_form.html',
        context,
        request=request
    )
    return JsonResponse(data)


def scheduling(request):
    if request.method == 'POST':
        form = BookingsForm(request.POST)

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.save()
            form.save_m2m()

            return HttpResponseRedirect('bookings/listagem/')
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            return render(request, 'bookings/scheduling_form.html', {'form':form})
    else:
        context = {'form': BookingsForm()}
        return render(request, 'bookings/scheduling_form.html', context)


def scheduling_edit(request, id_booking):
    booking = Booking.objects.get(id=id_booking)
    if request.method == 'GET':
        form = BookingsForm(instance=booking)
    else:
        form = BookingsForm(request.POST, instance=booking)
        if form.is_valid():
            new = form.save(commit=False)
            new.save()
            form.save_m2m()
        return HttpResponseRedirect('bookings/listagem/'+id_booking)
    return render(request, 'bookings/scheduling_form.html', {'form': form})

