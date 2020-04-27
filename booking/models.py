from django.db import models
from django.conf import settings

# Create your models here.
class Restaurant(models.Model):

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=255, unique=True)
    opening_time = models.FloatField()
    closing_time = models.FloatField()

    def __str__(self):
        return self.name


class Table(models.Model):
    
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='restaurants')
    size = models.IntegerField()
    number = models.IntegerField()
    currently_free = models.BooleanField(default=True)

    def __str__(self):
        return str(self.restaurant) + " " + str(self.number)


class Booking(models.Model):

    table = models.ManyToManyField(Table, related_name='tables')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='bookings')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created')
    created_at = models.DateTimeField(auto_now_add=True)
    people = models.IntegerField()
    booking_date_time_start = models.DateTimeField()
    booking_date_time_end = models.DateTimeField()
    booking_name = models.CharField(max_length=255)
    booking_email = models.CharField(max_length=255)
    booking_phone_number = models.CharField(max_length=255, null=True, blank=True)
    booking_confirmed = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        person = self.booking_name
        place = self.restaurant.name
        time = self.booking_date_time_start
        return person + " in " + place + " at " + str(time)
        
