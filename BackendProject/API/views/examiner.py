import math
import random
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
        except Examiner.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

class SingleExamView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        exam = Exam.objects.get(id = id)
        if exam.examiner.pk == request.user.id:
            
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
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request, id):
        whole_exam = self.get(request,id).data
        for key in whole_exam:
            if key == 'id':
                exam = Exam.objects.get(id = whole_exam[key])
            if key == 'exam':
                exam.exam_name = request.data['exam']
            if key == 'startdate':
                exam.exam_startdate = request.data['startdate']
            if key == 'duration':
                exam.exam_duration = request.data['duration']
                exam.save()
            if key == 'questions':
                for index in range(len(request.data['questions'])):
                    new_question = request.data['questions'][index]
                    try:
                        question = Question.objects.get(id = new_question['id'])
                    except:
                        break
                    question.text = new_question['text']
                    question.mark = new_question['mark']
                    question.save()
                    new_answers = new_question['answers']
                    for ans_key in new_answers:
                        answer = Answer.objects.get(id = ans_key)
                        answer.text = new_answers[ans_key]['text']
                        answer.is_correct = new_answers[ans_key]['is_correct']
                        answer.save()

                for new_q in request.data['questions']:
                    flag = True
                    for q in whole_exam['questions']:
                        if new_q['text'] == q['text']:
                            flag = False
                    if flag:
                        new_question = Question(exam = exam,text = new_q['text'], mark = new_q['mark'])
                        new_question.save()
                        for idx in new_q['answers']:
                            new_answer = Answer(question = new_question,text = new_q['answers'][idx]['text'],is_correct = new_q['answers'][idx]['is_correct'])
                            new_answer.save()

                for q in whole_exam['questions']:
                    flag = False
                    for new_q in request.data['questions']:
                        if new_q['text'] == q['text'] or new_q['id'] == q['id']:
                            flag = True
                    if not flag:
                        deleted_question = Question.objects.get(id = q['id'])
                        deleted_question.delete()
                
        return Response(status=status.HTTP_200_OK)

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
            if request.user.id == exam.examiner.pk:
                serializer.save(exam = exam)
                return Response(data = serializer.data, status=status.HTTP_201_CREATED)
            else :
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

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
            if request.user.id == question.exam.examiner.pk:
                serializer.save(question = question)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else: 
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


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
        exam = Exam.objects.get(id=id)
        if exam.examiner.pk == request.user.id:
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
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, id):
        try :
            allowed_studnts = AllowedStudents.objects.filter(exam = id)
            students_id = allowed_studnts.values('student')
            students_name = []
            exam = Exam.objects.get(id=id)
            if exam.examiner.pk == request.user.id:
                data = {}
                User = get_user_model()
                data['exam'] = exam.id
                for student in students_id:
                    user = User.objects.get(pk = student.get('student')).username
                    students_name.append(user)
                data['student'] = students_name            
                return Response(data = data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except AllowedStudents.DoesNotExist:
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
            exam = ExamResults.objects.filter(exam = id)
            if exam.examiner.pk == request.user.id:
                serializer = ExamResultSerializer(instance = exam, many = True)
                return Response(data = serializer.data,status=status.HTTP_200_OK )
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED )
        except ExamResults.DoesNotExist:
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
            student_answer = StudentAnswer.objects.filter(exam = id, student =  st)
            serializer = StudentAnswerSerializer(instance=student_answer, many=True)
            return Response(data = serializer.data, status= status.HTTP_202_ACCEPTED)
        except StudentAnswer.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)
        

class AddSupervisorView(APIView):
    permission_classes=[IsAuthenticated]

    def get_allowed_studnts(self, id):
        try:
            return AllowedStudents.objects.filter(exam=id)
        except AllowedStudents.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        try:
            User = get_user_model()
            supervisors = request.data['supervisor']
            num_of_supervisors = len(supervisors)
            exam = Exam.objects.get(id=id)
            if exam.examiner.pk == request.user.id:
                allowed_students = self.get_allowed_studnts(exam.id)
                num_of_allowed_students = len(allowed_students)
                num_of_assigend_students = math.floor(num_of_allowed_students / num_of_supervisors)
                extra_students = num_of_allowed_students - (num_of_assigend_students * num_of_supervisors)
                data = {}
                index = 0
                extra_index = 0
                for supervisor in supervisors:
                    user = User.objects.get(username = supervisor)
                    supervisorOb = Supervisor.objects.get(user = user)
                    data['supervisor'] = supervisorOb
                    for index in range(index,index+num_of_assigend_students):
                        allowed_students[index].supervisor = supervisorOb
                        allowed_students[index].save()
                    index += 1

                if extra_students > 0:
                    for extra_index in range(extra_index, extra_index+extra_students):
                        user = User.objects.get(username = supervisors[num_of_supervisors-1-extra_index])
                        supervisorOb = Supervisor.objects.get(user = user)
                        allowed_students[index+extra_index].supervisor = supervisorOb
                        allowed_students[index+extra_index].save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED )
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        