from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Examiner)
admin.site.register(Supervisor)
admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Answer)