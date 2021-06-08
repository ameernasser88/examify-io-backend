from django.urls import path , include
from . import views
from . views import examiner, student ,general

urlpatterns = [
    path('', general.index),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('exam/', examiner.ExamView.as_view()),
    path('exam/<str:id>/', examiner.SingleExamView.as_view()),
    path('exam/<str:id>/attendance/', examiner.AttendaceSheetView.as_view()),
    path('exam/<str:id>/statistics/', examiner.ExamStatisticsView.as_view()),
    path('exam/<str:pk>/question/', examiner.QuestionView.as_view()),
    path('exam/<str:pk>/question/<str:id>/', examiner.OneQuestionApi.as_view()),
    path('exam/question/<str:pk>/answer/', examiner.AnswerView.as_view()),
    path('exam/question/<str:pk>/answer/<str:id>/', examiner.OneAnswerView.as_view()),
    path('exam/<str:id>/allowed-students/', examiner.AllowedStudentsView.as_view()),
    path('exam/<str:id>/allowed-students/<str:st>/', examiner.OneAllowedStudentsView.as_view()),
    path('exam/<str:id>/start/', student.ExamView.as_view()),
    path('exam/<str:id>/submit/', student.SubmitExam.as_view()),
    path('exam/<str:id>/marks/', examiner.StudentMarksView.as_view()),
    path('exam/<str:id>/student/<str:st>/', examiner.StudentAnswerView.as_view()),
    path('exam/<str:id>/supervisors/', examiner.SupervisorView.as_view()),
    path('exam/<str:id>/supervisor/<str:sp>/', examiner.OneSupervisorView.as_view()),
    path('student/dashboard/',student.StudentDashboardView.as_view())
    
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


#Examiner:
# create exam:
#    exam/  POST
#     "exam_name"
#     "exam_startdate"
#     "exam_duration"