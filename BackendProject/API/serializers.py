from django.db.models.fields import Field
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Exam

class ExamSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Exam
        fields ='__all__'

class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = ('key', 'user')
