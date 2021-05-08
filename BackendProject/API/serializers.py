from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Exam, Question, Answer, AllowedStudents

class TokenSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField('get_user_type')
    def get_user_type(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.user.user_type
    class Meta:
        model = Token
        fields = ('key', 'user_type')

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

class AllowedStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllowedStudents
        fields = '__all__'