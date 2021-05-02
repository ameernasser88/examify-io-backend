from ..models import Answer, Exam, Question
from django.shortcuts import render
from requests.models import to_key_val_list
from rest_framework import serializers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from datetime import date, datetime, timedelta
from django.utils import timezone
import pytz


class ExamView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        exam = Exam.objects.get(id = id)
        exam_endtime = exam.exam_startdate + timedelta(hours = exam.exam_duration)

        if timezone.now() >= exam.exam_startdate and timezone.now() < exam_endtime:
            exam_info = {'exam_name':exam.exam_name,'exam_starttime':exam.exam_startdate, 'exam_duration':exam.exam_duration, 'questions':{}}
            questions = Question.objects.filter(exam = exam)
            exam_questions = {}
            for question in questions:
                exam_questions[question.text] = {'mark': question.mark, 'previous_question':question.previous_question,'answers':{}}
                exam_answers = {}
                answers = Answer.objects.filter(question = question)
                index = 0
                for answer in answers:
                    exam_answers[index] = answer.text
                    index += 1
                exam_questions[question.text]['answers'] = exam_answers
                exam_info['questions'] = exam_questions
            return Response(status=status.HTTP_200_OK,data = exam_info)
        return Response(status=status.HTTP_401_UNAUTHORIZED)




