from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..serializers import AllowedStudentSerializer, AnswerSerializer, ExamResultSerializer, ExamSerializer, QuestionSerializer, StudentAnswerSerializer
from ..models import *
from ..decorators import *
from rest_framework.throttling import UserRateThrottle

class UserMinThrottle(UserRateThrottle):
    scope = 'user_min'

class UserDayThrottle(UserRateThrottle):
    scope = 'user_day'

#@method_decorator(examiners_only, name='dispatch')
class ExamView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes= [
        UserMinThrottle,
        UserDayThrottle
    ]
    def post(self, request):
        try:
            user = Examiner.objects.get(user = request.user)
            serializer = ExamSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save(examiner = user)
                # exam_id = serializer.data['id']
                # exam = Exam.objects.get(pk = exam_id)
                # exam.examiner = user
                # exam.save() 
                return Response(serializer.data,status= status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Examiner.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
    
    def get(self, request):
        try:
            examiner = Examiner.objects.get(user = request.user)
            exams = Exam.objects.filter(examiner = examiner)
            serializer = ExamSerializer(instance = exams, many = True)
            return Response(data= serializer.data, status= status.HTTP_200_OK)
        except Examiner.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

#@method_decorator(examiners_only, name='dispatch')
class QuestionView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes= [
        UserMinThrottle,
        UserDayThrottle
    ]
    def post(self, request, pk):
        exam = Exam.objects.get(id = pk)
        serializer = QuestionSerializer(data = request.data)
        if serializer.is_valid():
            if request.user.id == exam.examiner.pk:
                serializer.save(exam = exam)
                return Response(data = serializer.data, status=status.HTTP_201_CREATED)
            else :
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

#@method_decorator(examiners_only, name='dispatch')
class AnswerView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes= [
        UserMinThrottle,
        UserDayThrottle
    ]
    def post(self, request, pk):
        question = Question.objects.get(id = pk)
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            if request.user.id == question.exam.examiner.pk:
                serializer.save(question = question)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else: 
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


#@method_decorator(examiners_only, name='dispatch')
class AllowedStudentsView(APIView):
    throttle_classes= [
        UserMinThrottle,
        UserDayThrottle
    ]
    permission_classes=[IsAuthenticated]
    def post(self, request, id):
        User = get_user_model()
        usernames = request.data['students']
        exam = Exam.objects.get(id=id)
        data = {}
        data['exam'] = exam.id
        for username in usernames:
            user = User.objects.get(username = username)
            student = Student.objects.get(user = user)
            data['student'] = student
            serializer = AllowedStudentSerializer(data = data)

            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

                
        
    def get(self, request, id):
        try :
            allowed_studnts = AllowedStudents.objects.filter(exam = id)
            students_id = allowed_studnts.values('student')
            students_name = []
            exam = Exam.objects.get(id=id)
            data = {}
            User = get_user_model()
            data['exam'] = exam.id
            for student in students_id:
                user = User.objects.get(pk = student.get('student')).username
                students_name.append(user)
            data['student'] = students_name            
            return Response(data = data, status=status.HTTP_200_OK)
        except AllowedStudents.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

#@method_decorator(examiners_only, name='dispatch')
class StudentMarksView(APIView):
    throttle_classes= [
        UserMinThrottle,
        UserDayThrottle
    ]
    permission_classes=[IsAuthenticated]
    def get(self, request, id):
        try:
            exam = ExamResults.objects.filter(exam = id)
            serializer = ExamResultSerializer(instance = exam, many = True)
            
            return Response(data = serializer.data,status=status.HTTP_200_OK )
        except ExamResults.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

#@method_decorator(examiners_only, name='dispatch')
class StudentAnswerView(APIView):
    throttle_classes= [
        UserMinThrottle,
        UserDayThrottle
    ]
    permission_classes=[IsAuthenticated]
    def get(self, request, id, st):
        try:
            student_answer = StudentAnswer.objects.filter(exam = id, student =  st)
            serializer = StudentAnswerSerializer(instance=student_answer, many=True)
            return Response(data = serializer.data, status= status.HTTP_202_ACCEPTED)
        except StudentAnswer.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)
        
