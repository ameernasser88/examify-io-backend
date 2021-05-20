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

#@method_decorator(students_only, name='dispatch')
class ExamView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            exam = Exam.objects.get(id = id)
        except Exam.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        mins,hrs = math.modf(exam.exam_duration)
        exam_endtime = exam.exam_startdate + timedelta(hours = hrs, minutes=mins*60)
        allowed_students = AllowedStudents.objects.filter(exam = exam)
        error = {}
        if not allowed_students.filter(student = request.user.pk):
            error['error'] = ErrorMessages.objects.get(id = 1).error_message
            return Response(data = error, status=status.HTTP_401_UNAUTHORIZED )
        if not timezone.now() >= exam.exam_startdate :
            error['error'] = ErrorMessages.objects.get(id = 3).error_message
            return Response(data = error,status=status.HTTP_401_UNAUTHORIZED)
        if not timezone.now() < exam_endtime:
            error['error'] = ErrorMessages.objects.get(id = 2).error_message
            return Response(data = error,status=status.HTTP_401_UNAUTHORIZED)

        student = Student.objects.get(user = request.user)
        allowed_student = AllowedStudents.objects.get(student = student , exam=exam)
        allowed_student.enter_time = timezone.now()
        allowed_student.attendance = True
        allowed_student.save()
        exam_info = {'exam_name':exam.exam_name,'exam_starttime':exam.exam_startdate, 'exam_duration':exam.exam_duration, 'questions':{}}
        questions = Question.objects.filter(exam = exam)
        exam_questions = {}
        for question in questions:
            exam_questions[question.text] = {'mark': question.mark, 'previous_question':question.previous_question,'answers':{}}
            exam_answers = {}
            answers = Answer.objects.filter(question = question)
            for answer in answers:
                exam_answers[answer.id] = answer.text
            exam_questions[question.text]['answers'] = exam_answers
            exam_info['questions'] = exam_questions
        return Response(status=status.HTTP_200_OK,data = exam_info)

#@method_decorator(students_only, name='dispatch')
class SubmitExam(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, id):
        user = request.user
        student = Student.objects.get(user=user)
        exam = Exam.objects.get(id=id)
        if (student is None) or (exam is None):
            return Response(status = status.HTTP_404_NOT_FOUND)

        student_answers = request.data['student_answers']
        try:
            total_mark = 0
            for question_id, answer_id in student_answers.items():
                question_id = int(question_id)
                answer = Answer.objects.get(id=answer_id)
                question = Question.objects.get(id=question_id)
                student_answer = StudentAnswer(
                    student=student,
                    exam = exam,
                    answer = answer,
                    question = question
                )
                student_answer.save()
                if answer.is_correct:
                    total_mark = total_mark + question.mark
            exam_result = ExamResults(student=student,exam=exam,mark=total_mark)
            exam_result.save()
            allowed_student = AllowedStudents.objects.get(student = student)
            allowed_student.submit_time = timezone.now()
            allowed_student.save()
            return Response(status = status.HTTP_200_OK)
        except:
            return Response(status = status.HTTP_404_NOT_FOUND)






