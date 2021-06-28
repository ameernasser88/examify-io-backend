from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..models import *
from ..serializers import SupervisorDashboardSerializer


class SupervisorDashboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user = Supervisor.objects.get(user = request.user.pk)
            exams_to_supervise = ExamSupervisors.objects.filter(supervisor = user).values('exam')
            exam = []
            for e in exams_to_supervise:
                exam.append(e['exam'])
            serializer = SupervisorDashboardSerializer(exam, many = True) 
            return Response(data = serializer.data,status = status.HTTP_200_OK)
        except :
            return Response(status=status.HTTP_404_NOT_FOUND)

class OneExamToSuperviseView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            exam = Exam.objects.get(id = id)
            user = Supervisor.objects.get(user = request.user.pk)
            data = {}
            students = []
            students_id = AllowedStudents.objects.filter(exam = exam, supervisor = user).values('student')
            for st in students_id:
                one_stu = {}
                stu_obj = Student.objects.get(user_id = st['student'])
                one_stu['student_id'] = stu_obj.user_id
                one_stu['student_name'] = stu_obj.user.username
                students.append(one_stu)
            data['exam_id'] = exam.id
            data['exam_name'] = exam.exam_name
            data['exam_startdate'] = exam.exam_startdate
            data['exam_duration'] = exam.exam_duration
            data['students'] = students
            return Response(data = data, status = status.HTTP_200_OK)
        except :
            return Response(status=status.HTTP_404_NOT_FOUND)



