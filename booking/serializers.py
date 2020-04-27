from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from booking import models
from django.db import transaction


class TableSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Table
        fields = '__all__'

class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Restaurant
        fields = '__all__'

    def to_representation(self, instance):
        data = super(RestaurantSerializer, self).to_representation(instance)
        data['tables'] = TableSerializer(instance.restaurants.all().order_by('id'), many=True).data
        return data

class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Booking
        fields = '__all__'

    @transaction.atomic
    def save(self):
        data = self.validated_data
        booking = super().save()
        booking.booking_confirmed = True
        for table in data['table']:
            table.currently_free = False
            table.save()
            booking.table.add(table)
        booking.save()
        return booking

    def to_representation(self, instance):
        return_data = super().to_representation(instance)
        return_data['restaurant'] = RestaurantSerializer(instance.restaurant).data
        return return_data

class BookingCancelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Booking
        fields = ('is_cancelled',)