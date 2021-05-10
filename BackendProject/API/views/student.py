from django.utils.decorators import method_decorator
from ..models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from datetime import timedelta
from django.utils import timezone
from ..decorators import *

@method_decorator(students_only, name='dispatch')
class ExamView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            exam = Exam.objects.get(id = id)
        except Exam.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        exam_endtime = exam.exam_startdate + timedelta(hours = exam.exam_duration)
        allowed_students = AllowedStudents.objects.filter(exam = exam)
        if allowed_students.filter(student = request.user.pk):
            if timezone.now() >= exam.exam_startdate :
                if timezone.now() < exam_endtime:
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
                else:
                    error = {}
                    error['error'] = ErrorMessages.objects.get(id = 2).error_message
                    return Response(data = error,status=status.HTTP_401_UNAUTHORIZED)
            else:
                error = {}
                error['error'] = ErrorMessages.objects.get(id = 3).error_message
                return Response(data = error,status=status.HTTP_401_UNAUTHORIZED)
        else:
            error = {}
            error['error'] = ErrorMessages.objects.get(id = 1).error_message
            return Response(data = error, status=status.HTTP_401_UNAUTHORIZED )
        




