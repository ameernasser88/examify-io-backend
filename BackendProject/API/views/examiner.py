import math
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils.decorators import method_decorator
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..serializers import AllowedStudentSerializer, AnswerSerializer, AssignedSupervisors, AttendanceSheetSerializer, ExamResultSerializer, ExamSerializer, QuestionSerializer, StudentAnswerSerializer, SupervisorSerializer
from ..models import *
from ..decorators import *
from rest_framework.throttling import UserRateThrottle

def get_allowed_studnts(id):
    try:
        return AllowedStudents.objects.filter(exam=id)
    except AllowedStudents.DoesNotExist:
        raise Response(status=status.HTTP_404_NOT_FOUND)


def reassign_supervisors_to_students(supervisors, exam):
    num_of_supervisors = len(supervisors)
    if num_of_supervisors == 0:
        return None
    allowed_students = get_allowed_studnts(exam.id)
    num_of_allowed_students = len(allowed_students)

    super_index = 0
    for student in allowed_students:
        if super_index >= num_of_supervisors:
            super_index = 0
        user = User.objects.get(username = supervisors[super_index])
        supervisorOb = Supervisor.objects.get(user = user)
        student.supervisor = supervisorOb
        student.save()
        super_index +=1
    return None

# class UserMinThrottle(UserRateThrottle):
#     scope = 'user_min'

# class UserDayThrottle(UserRateThrottle):
#     scope = 'user_day'

#@method_decorator(examiners_only, name='dispatch')
class ExamView(APIView):
    permission_classes = [IsAuthenticated]
    # throttle_classes= [
    #     UserMinThrottle,
    #     UserDayThrottle
    # ]
    def post(self, request):
        try:
            user = Examiner.objects.get(user = request.user)
            serializer = ExamSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save(examiner = user)
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
        except :
            return Response(status = status.HTTP_404_NOT_FOUND)

class SingleExamView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        exam = Exam.objects.get(id = id)
        if exam.examiner.pk != request.user.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED )
        questions = Question.objects.filter(exam = exam)
        data = {}
        data['id'] = exam.id
        data['exam'] = exam.exam_name
        data['startdate'] = exam.exam_startdate
        data['duration'] = exam.exam_duration
        ques = {}
        all_questions = []
        for question in questions:
            ques['id'] = question.id
            ques['text'] = question.text
            ques['mark'] = question.mark
            answers = Answer.objects.filter(question = question)
            ans = {}
            for answer in answers:
                ans[answer.id] = {'text':answer.text, 'is_correct':answer.is_correct}
            ques['answers'] = ans
            all_questions.append(ques)
            ques = {}
        data['questions'] = all_questions
        return Response(data = data , status=status.HTTP_200_OK)

    def patch(self, request, id):
        try:
            exam = Exam.objects.get(id = id)
            if exam.examiner.pk != request.user.id:
                return Response(status=status.HTTP_401_UNAUTHORIZED )
            exam.exam_name = request.data['exam']
            exam.exam_startdate = request.data['startdate']
            exam.exam_duration = request.data['duration']
            exam.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status = status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            deleted_exam = Exam.objects.get(id = id)
            if request.user.id != deleted_exam.examiner.pk:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
            deleted_exam.delete()
            return Response(status=status.HTTP_200_OK)
        except :
            return Response(status=status.HTTP_404_NOT_FOUND)


#@method_decorator(examiners_only, name='dispatch')
class QuestionView(APIView):
    permission_classes = [IsAuthenticated]
    # throttle_classes= [
    #     UserMinThrottle,
    #     UserDayThrottle
    # ]
    def post(self, request, pk):
        exam = Exam.objects.get(id = pk)
        serializer = QuestionSerializer(data = request.data)
        if serializer.is_valid():
            if request.user.id != exam.examiner.pk:
                return Response(status=status.HTTP_401_UNAUTHORIZED )
            serializer.save(exam = exam)
            return Response(data = serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class OneQuestionApi(APIView):
    permission_classes= [IsAuthenticated]
    def delete(self, request, pk , id):
        try:
            deleted_question = Question.objects.get(id = id)
            if request.user.id != deleted_question.exam.examiner.pk:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
            deleted_question.delete()
            return Response(status=status.HTTP_200_OK)
        except :
            return Response(status=status.HTTP_404_NOT_FOUND)


    def patch(self, request, pk, id):
        try:
            question = Question.objects.get(id = id)
            if request.user.id != question.exam.examiner.pk:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            question.text = request.data['text']
            question.mark = request.data['mark']
            question.save()
            return Response(status=status.HTTP_200_OK)
        except :
            return Response(status=status.HTTP_404_NOT_FOUND)


#@method_decorator(examiners_only, name='dispatch')
class AnswerView(APIView):
    permission_classes = [IsAuthenticated]
    # throttle_classes= [
    #     UserMinThrottle,
    #     UserDayThrottle
    # ]
    def post(self, request, pk):
        question = Question.objects.get(id = pk)
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            if request.user.id != question.exam.examiner.pk:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            serializer.save(question = question)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class OneAnswerView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk, id):
        try:
            deleted_answer = Answer.objects.get(id = id)
            if request.user.id != deleted_answer.question.exam.examiner.pk:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
            deleted_answer.delete()
            return Response(status=status.HTTP_200_OK)
        except Answer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk, id):
        try:
            answer = Answer.objects.get(id = id)
            if request.user.id != answer.question.exam.examiner.pk:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            answer.text = request.data['text']
            answer.is_correct = request.data['is_correct']
            answer.save()
            return Response(status=status.HTTP_200_OK)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class AttendaceSheetView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            exam = Exam.objects.get(id = id)
            if request.user.id != exam.examiner.pk:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            attendance = AllowedStudents.objects.filter(exam = exam, attendance = True)
            serializer = AttendanceSheetSerializer(instance = attendance, many = True)
            return Response(data = serializer.data,status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)



#@method_decorator(examiners_only, name='dispatch')
class AllowedStudentsView(APIView):
    # throttle_classes= [
    #     UserMinThrottle,
    #     UserDayThrottle
    # ]

    permission_classes=[IsAuthenticated]
    def post(self, request, id):
        User = get_user_model()
        usernames = request.data['students']
        try:
            exam = Exam.objects.get(id=id)
            if request.user.id != exam.examiner.pk:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            
            data = {}
            data['exam'] = exam.id
            for username in usernames:
                user = User.objects.get(username = username)
                student = Student.objects.get(user = user)
                allowed_students = AllowedStudents.objects.filter(exam = exam, student = student)
                if allowed_students:
                    continue
                data['student'] = student
                data['id'] = user.id
                supervisors_ids = AllowedStudents.objects.filter(exam = exam).values('supervisor').annotate(total=Count('supervisor')).order_by('total')
                serializer = AllowedStudentSerializer(data = data)
                if serializer.is_valid():
                    serializer.save()
                    supervisors = []
                    for supervisor in supervisors_ids:
                        if supervisor['supervisor'] is None:
                            continue
                        supervisor_name = User.objects.get(id=supervisor['supervisor'])
                        supervisors.append(supervisor_name.username)
                    reassign_supervisors = reassign_supervisors_to_students(supervisors, exam)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_201_CREATED)
                
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        try :
            allowed_studnts = AllowedStudents.objects.filter(exam = id)
            students_id = allowed_studnts.values('student')
            students_name = []
            exam = Exam.objects.get(id=id)
            if exam.examiner.pk != request.user.id:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            data = {}
            User = get_user_model()
            data['exam'] = exam.id
            for student in students_id:
                user = User.objects.get(pk = student.get('student')).username
                students_name.append(user)
            data['student'] = students_name            
            return Response(data = data, status=status.HTTP_200_OK)
        except:
            return Response(status = status.HTTP_404_NOT_FOUND)

class OneAllowedStudentsView(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self, request, id, st):
        try:
            User= get_user_model()
            user = User.objects.get(id = st)
            student = Student.objects.get(user = user)
            exam = Exam.objects.get(id = id)
            if request.user.id != exam.examiner.pk:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            allowed_student = AllowedStudents.objects.get(student = student, exam = exam)
            allowed_student.delete()
            supervisors_ids = AllowedStudents.objects.filter(exam = exam).values('supervisor').annotate(total=Count('supervisor')).order_by('total')
            supervisors = []
            for supervisor in supervisors_ids:
                if supervisor['supervisor'] is None:
                    continue
                supervisor_name = User.objects.get(id=supervisor['supervisor'])
                supervisors.append(supervisor_name.username)
            reassign_supervisors = reassign_supervisors_to_students(supervisors, exam)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status = status.HTTP_404_NOT_FOUND)


#@method_decorator(examiners_only, name='dispatch')
class StudentMarksView(APIView):
    # throttle_classes= [
    #     UserMinThrottle,
    #     UserDayThrottle
    # ]
    permission_classes=[IsAuthenticated]
    def get(self, request, id):
        try:
            exam = Exam.objects.get(id=id)
            qs = ExamResults.objects.filter(exam=exam)
            if exam.examiner.pk != request.user.id:
                return Response(status=status.HTTP_401_UNAUTHORIZED )
            serializer = ExamResultSerializer(qs, many = True)
            return Response(data = serializer.data,status=status.HTTP_200_OK )
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

#@method_decorator(examiners_only, name='dispatch')
class StudentAnswerView(APIView):
    # throttle_classes= [
    #     UserMinThrottle,
    #     UserDayThrottle
    # ]
    permission_classes=[IsAuthenticated]
    def get(self, request, id, st):
        try:
            exam = Exam.objects.get(id=id)
            student = Student.objects.get(user_id=st)
            if exam.examiner.pk != request.user.id:
                return Response(status=status.HTTP_401_UNAUTHORIZED )
            student_answers = StudentAnswer.objects.filter(exam=exam, student = student)
            serializer = StudentAnswerSerializer(student_answers, many=True)
            return Response(data = serializer.data, status= status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

class SupervisorView(APIView):
    permission_classes=[IsAuthenticated]
    def patch(self, request, id):
        try:
            User = get_user_model()
            supervisors = request.data['supervisor']
            exam = Exam.objects.get(id=id)
            if exam.examiner.pk != request.user.id:
                return Response(status=status.HTTP_401_UNAUTHORIZED )
            assign_supervisors = reassign_supervisors_to_students(supervisors,exam)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, id):
        try:
            exam = Exam.objects.get(id = id)
            if exam.examiner.pk != request.user.id:
                return Response(status=status.HTTP_401_UNAUTHORIZED )
            allowed_students = AllowedStudents.objects.filter(exam = exam)
            serializer = AssignedSupervisors(instance=allowed_students, many = True)
            return Response(data = serializer.data, status=status.HTTP_200_OK)
        except :
            return Response(status=status.HTTP_404_NOT_FOUND)
