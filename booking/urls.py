from django.urls import path
from rest_framework import routers
from booking import views as api_views

router = routers.SimpleRouter()
router.register(r'api/v1/restaurants', api_views.RestaurantViewSet, basename='restaurants')
router.register(r'api/v1/bookings', api_views.BookingViewSet, basename='bookings')
urlpatterns = [
] + router.urls