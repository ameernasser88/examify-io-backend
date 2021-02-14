from django.urls import path , include
from . import views
from rest_framework.routers import DefaultRouter
from . views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls'))
]
