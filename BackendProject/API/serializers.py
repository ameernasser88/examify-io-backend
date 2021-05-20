from django.db.models import fields
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import *

class TokenSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField('get_user_type')
    def get_user_type(self, obj):
        request = self.context.get('request', None)
        if request.user.is_anonymous:
            return None
        else:
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
        fields = ('student','exam')

class AttendanceSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllowedStudents
        fields = ('id','student_name','supervisor_name','enter_time','submit_time')
    student_name = serializers.SerializerMethodField('get_student_name')
    supervisor_name = serializers.SerializerMethodField('get_supervisor_name')

    def get_student_name(self, obj):
        user = User.objects.get(pk = obj.student.pk)
        return user.username
    def get_supervisor_name(self, obj):
        user = User.objects.get(pk = obj.supervisor.pk)
        return user.username

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('username')

class SupervisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supervisor
        fields = ('username')

class AssignedSupervisors(serializers.ModelSerializer):
    class Meta:
        model = AllowedStudents
        fields = ('id','supervisor_name', 'student_name')
    student_name = serializers.SerializerMethodField('get_student_name')
    def get_student_name(self, obj):
        user = User.objects.get(pk = obj.student.pk)
        return user.username
    supervisor_name = serializers.SerializerMethodField('get_supervisor_name')
    def get_supervisor_name(self, obj):
        user = User.objects.get(pk = obj.supervisor.pk)
        return user.username

class ExamResultSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ExamResults
        fields = ('student', 'student_name', 'mark')

    student_name = serializers.SerializerMethodField('get_student_name')
    def get_student_name(self, obj):
        return obj.student.user.username

class StudentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = ('student_name', 'student','exam', 'exam_name', 'question', 'question_text', 'answer', 'answer_text', 'is_correct')

    exam_name = serializers.SerializerMethodField('get_exam_name')
    student_name = serializers.SerializerMethodField('get_student_name')
    question_text = serializers.SerializerMethodField('get_question_text')
    answer_text = serializers.SerializerMethodField('get_answer_text')
    is_correct = serializers.SerializerMethodField('is_answer_correct')


    def get_exam_name(self, obj):
        exam = Exam.objects.get(id = obj.exam.id)
        return exam.exam_name

    def get_student_name(self, obj):
        user = User.objects.get(pk = obj.student.pk)
        return user.username

    
    def get_question_text(self, obj):
        question = Question.objects.get(id = obj.exam.id)
        return question.text

    def get_answer_text(self, obj):
        answer = Answer.objects.get(id = obj.answer.id)
        return answer.text

    def is_answer_correct(self, obj):
        answer = Answer.objects.get(id = obj.answer.id)
        return answer.is_correct