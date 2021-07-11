from ..serializers import *
import math
from django.utils.decorators import method_decorator
from ..models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from datetime import timedelta
from django.utils import timezone
from ..decorators import *
import  json
import requests



# @method_decorator(students_only, name='dispatch')
class ExamView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            exam = Exam.objects.get(id=id)
        except Exam.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        mins, hrs = math.modf(exam.exam_duration)
        exam_endtime = exam.exam_startdate + timedelta(hours=hrs, minutes=mins * 60)
        allowed_students = AllowedStudents.objects.filter(exam=exam)
        error = {}
        if not allowed_students.filter(student=request.user.pk):
            error['error'] = ErrorMessages.objects.get(id=1).error_message
            return Response(data=error, status=status.HTTP_401_UNAUTHORIZED)
        if not timezone.now() >= exam.exam_startdate:
            error['error'] = ErrorMessages.objects.get(id=3).error_message
            return Response(data=error, status=status.HTTP_401_UNAUTHORIZED)
        if not timezone.now() < exam_endtime:
            error['error'] = ErrorMessages.objects.get(id=2).error_message
            return Response(data=error, status=status.HTTP_401_UNAUTHORIZED)

        student = Student.objects.get(user=request.user)
        allowed_student = AllowedStudents.objects.get(student=student, exam=exam)
        allowed_student.enter_time = timezone.now()
        allowed_student.attendance = True
        allowed_student.save()
        exam_info = {'exam_name': exam.exam_name, 'exam_starttime': exam.exam_startdate,
                     'exam_duration': exam.exam_duration, 'questions': {}}
        questions = Question.objects.filter(exam=exam)
        exam_questions = {}
        for question in questions:
            exam_questions[question.id] = {'text': question.text, 'mark': question.mark,
                                           'previous_question': question.previous_question, 'answers': {}}
            exam_answers = {}
            answers = Answer.objects.filter(question=question)
            for answer in answers:
                exam_answers[answer.id] = answer.text
            exam_questions[question.id]['answers'] = exam_answers
            exam_info['questions'] = exam_questions
        return Response(status=status.HTTP_200_OK, data=exam_info)


# @method_decorator(students_only, name='dispatch')
class SubmitExam(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        user = request.user
        student = Student.objects.get(user=user)
        exam = Exam.objects.get(id=id)
        if (student is None) or (exam is None):
            return Response(status=status.HTTP_404_NOT_FOUND)

        submitted = ExamResults.objects.filter(student=student, exam=exam).count()
        if submitted != 0:
            error = {}
            error['error'] = ErrorMessages.objects.get(id=5).error_message
            return Response(data=error, status=status.HTTP_401_UNAUTHORIZED)

        student_answers = request.data['student_answers']
        try:
            total_mark = 0
            for question_id, answer_id in student_answers.items():
                question_id = int(question_id)
                answer = Answer.objects.get(id=answer_id)
                question = Question.objects.get(id=question_id)
                student_answer = StudentAnswer(
                    student=student,
                    exam=exam,
                    answer=answer,
                    question=question
                )
                student_answer.save()
                if answer.is_correct:
                    total_mark = total_mark + question.mark
            exam_result = ExamResults(student=student, exam=exam, mark=total_mark)
            exam_result.save()
            allowed_student = AllowedStudents.objects.get(student=student, exam=exam)
            allowed_student.submit_time = timezone.now()
            allowed_student.attendance = True
            allowed_student.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class StudentDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = Student.objects.get(user=request.user.pk)
        student_exams = AllowedStudents.objects.filter(student=user)
        serializer = StudentAllExamsSerializer(student_exams, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


####### Programming ##########################################3

class StudentProgrammingTestsDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = Student.objects.get(user=request.user.pk)
        student_exams = ProgrammingTestAllowedStudents.objects.filter(student=user)
        serializer = StudentAllProgrammingTestsSerializer(student_exams, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class ProgrammingTestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            test = ProgrammingTest.objects.get(id=id)
        except ProgrammingTest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        mins, hrs = math.modf(test.test_duration)
        test_endtime = test.test_startdate + timedelta(hours=hrs, minutes=mins * 60)
        allowed_students = ProgrammingTestAllowedStudents.objects.filter(test=test)
        error = {}
        if not allowed_students.filter(student=request.user.pk):
            error['error'] = ErrorMessages.objects.get(id=1).error_message
            return Response(data=error, status=status.HTTP_401_UNAUTHORIZED)
        if not timezone.now() >= test.test_startdate:
            error['error'] = ErrorMessages.objects.get(id=3).error_message
            return Response(data=error, status=status.HTTP_401_UNAUTHORIZED)
        if not timezone.now() < test_endtime:
            error['error'] = ErrorMessages.objects.get(id=2).error_message
            return Response(data=error, status=status.HTTP_401_UNAUTHORIZED)

        student = Student.objects.get(user=request.user)
        allowed_student = ProgrammingTestAllowedStudents.objects.get(student=student, test=test)
        allowed_student.enter_time = timezone.now()
        allowed_student.attendance = True
        allowed_student.save()
        test_info = {'test_name': test.test_name, 'test_starttime': test.test_startdate,
                     'test_duration': test.test_duration, 'questions': {}}
        questions = ProgrammingQuestion.objects.filter(test=test)
        test_questions = {}
        for question in questions:
            test_questions[question.id] = question.text

        test_info['questions'] = test_questions
        return Response(status=status.HTTP_200_OK, data=test_info)


class SubmitProgrammingTest(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        user = request.user
        student = Student.objects.get(user=user)
        test = ProgrammingTest.objects.get(id=id)
        if (student is None) or (test is None):
            return Response(status=status.HTTP_404_NOT_FOUND)

        student_answers = request.data['student_answers']
        # "student_answers": { "18" : ["java" , "--code--"], "19" : ["python3" , "--code--"] }
        for question_id, arr in student_answers.items():
            escaped = arr[1].translate(str.maketrans({"-": r"\-",
                                                      "]": r"\]",
                                                      "\\": r"\\",
                                                      "^": r"\^",
                                                      "$": r"\$",
                                                      "*": r"\*",
                                                      ".": r"\."}))
            print(escaped)
            print(arr[0])
            url = "https://api.jdoodle.com/v1/execute/"
            payload = {"clientId":"9d32bd85ad32dd4e5f5b4edf2675ea97",
                       "clientSecret":"b80cbecc9e149e9aed7511bc3df0935a6edcb2ee3cee2233714f2432199e06c1"  ,
                       "stdin" :"",
                       "script":arr[1],
                       "language":arr[0],
                       "versionIndex":"4"}
            response = requests.post(url, data=payload, verify=False)
            print(response.content)

        return Response(status=status.HTTP_200_OK)
