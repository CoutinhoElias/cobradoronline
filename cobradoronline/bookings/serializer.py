# from django.contrib.auth.models import User
from rest_framework import serializers

#from cobradoronline.users.models import User
from cobradoronline.bookings.models import Booking


class BookingSerializer(serializers.HyperlinkedModelSerializer):

    # user = serializers.PrimaryKeyRelatedField(
    #     read_only=False,
    #     queryset=User.objects.all()
    # )

    class Meta:
        model = Booking
        fields = ('title', 'start', 'end','created_on', 'authorized', 'color')
