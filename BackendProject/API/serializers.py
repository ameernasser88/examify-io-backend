from django.db.models import fields
from django.db.models.fields import Field
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Exam, Question, Answer

class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = ('key', 'user')

class ExamSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Exam
        fields ='__all__'

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

