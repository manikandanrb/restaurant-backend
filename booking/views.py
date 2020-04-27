from django.shortcuts import render
from django.http import Http404, HttpResponse
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import response, status
from booking import models, serializers
from rest_framework.decorators import action
from django.db import transaction

# Create your views here.

class RestaurantViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, )
    permissions = (IsAuthenticated, )

    serializer_class = serializers.RestaurantSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = models.Restaurant.objects.filter()
        return queryset

class BookingViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, )
    permissions = (IsAuthenticated, )
    serializer_class = serializers.BookingSerializer
    cancel_serializer_class = serializers.BookingCancelSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = models.Booking.objects.filter(created_by=user)
        return queryset

    def create(self, request):        
        data = request.data.copy()
        context = {
            'request': request
        }
        data['created_by'] = request.user.id
        serializer = self.serializer_class(data=data, context=context)
        if serializer.is_valid():
            serializer.save()
            data = {
                "status":"success"
            }
            return response.Response(status=status.HTTP_201_CREATED,
                                     data=data)
        else:
            return response.Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                     data=serializer.errors)

    @action(detail=True, methods=['post'], url_path='cancel-booking')
    def cancel_booking(self, request, pk=None):
        booking = self.get_queryset().get(pk=pk)
        data = request.data.copy()
        serializer = self.cancel_serializer_class(data=data)
        if not serializer.is_valid():
            return response.Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data=serializer.errors)
        else:
            with transaction.atomic():
                tables = booking.table.all()
                for table in tables:
                    table.currently_free = True
                    table.save()
                booking.is_cancelled = True
                booking.save()
            report_data = self.serializer_class(instance=booking).data
            return response.Response(status=status.HTTP_200_OK, data=report_data)


def index(request):
    return render(request, 'restaurant.html')