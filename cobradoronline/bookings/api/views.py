from django.shortcuts import redirect
from rest_framework.generics import (
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    CreateAPIView, get_object_or_404)
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from cobradoronline.bookings.models import Booking
from cobradoronline.bookings.serializer import BookingSerializer
from .serializers import (BookingListSerializer,
                          BookingDetailSerializer,
                          BookingCreateUpdateSerializer, BookingListFeriadoSerializer)


class PostCreateAPIView(CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingCreateUpdateSerializer

class PostDetailAPIView(RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingDetailSerializer
    # lookup_field = 'user'


class PostUpdateAPIView(UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingCreateUpdateSerializer
    lookup_field = 'pk'


class PostDeleteAPIView(DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingDetailSerializer
    lookup_field = 'pk'


class PostListAPIView(ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingListSerializer

class PostListFeriadoAPIView(ListAPIView):
    queryset = Booking.objects.filter(holiday=True)
    serializer_class = BookingListFeriadoSerializer

#------------------------------------------------------------------------------------


class PostList2APIView(ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'profile_list.html'

    def get(self, request):
        queryset = Booking.objects.all()
        return Response({'bookings': queryset})

class PostUpdate2APIView(UpdateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'profile_detail.html'

    def get(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        serializer = BookingSerializer(booking)
        return Response({'serializer': serializer, 'booking': booking})

    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        serializer = BookingSerializer(booking, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'booking': booking})
        serializer.save()
        return redirect('profile-list')