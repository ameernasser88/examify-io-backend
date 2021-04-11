from django.urls import path , include
from . import views
from rest_framework.routers import DefaultRouter
from . views import examiner
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('exam/', examiner.ExamApi.as_view() )
]


# # # Authentication # # #

# /dj-rest-auth/registration/ (POST)
#
# username
# password1
# password2
# email
# user_type

# /dj-rest-auth/login/ (POST)
#
# username
# email ( not required )
# password

#/dj-rest-auth/logout/ (POST)

# /dj-rest-auth/password/reset/ (POST)
#
# email
#
# /dj-rest-auth/password/reset/confirm/ (POST)
#
# uid
# token
# new_password1
# new_password2
#
# /dj-rest-auth/password/change/ (POST)
#
# new_password1
# new_password2
# old_password
#
# /dj-rest-auth/user/ (GET, PUT, PATCH)
#
# username
# first_name
# last_name
# Returns pk, username, email, first_name, last_name
#

# /dj-rest-auth/registration/verify-email/ (POST)
#
# key