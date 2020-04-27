from django.urls import path
from users.views import login, logout, signup, profile

urlpatterns = [
    path('api/v1/signup/', signup),
    path('api/v1/login/', login),
    path('api/v1/logout/', logout),
    path('api/v1/profile/', profile),
]