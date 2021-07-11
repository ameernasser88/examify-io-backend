from datetime import timedelta
import math
from django.db.models import fields
from django.utils import timezone
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


class ProgrammingTestSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProgrammingTest
        fields ='__all__'

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class ProgrammingQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammingQuestion
        fields = '__all__'

class StudentProgrammingAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProgrammingAnswer
        fields = '__all__'



class ProgrammingTestAllowedStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammingTestAllowedStudents
        fields = '__all__'

class AllowedStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllowedStudents
        fields = ('id','student','exam')

class AttendanceSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllowedStudents
        fields = ('id','student_name','supervisor_name','enter_time','submit_time')
    student_name = serializers.SerializerMethodField('get_student_name')
    supervisor_name = serializers.SerializerMethodField('get_supervisor_name')
    id = serializers.SerializerMethodField('get_student_id')

    def get_student_name(self, obj):
        user = User.objects.get(pk = obj.student.pk)
        return user.username
    def get_supervisor_name(self, obj):
        user = User.objects.get(pk = obj.supervisor.pk)
        return user.username
    def get_student_id(self, obj):
        user = User.objects.get(pk = obj.student.pk)
        return user.id

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('username')

class SupervisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supervisor
        fields = ('username')

class AddSupervisorToExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamSupervisors
        fields = '__all__'

class StudentAllExamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllowedStudents
        fields = ('exam_id','exam_name','exam_startdate','exam_duration','student_id','student_name', 'full_mark', 'student_mark', 'is_started')
    student_name = serializers.SerializerMethodField('get_student_name')
    student_id = serializers.SerializerMethodField('get_student_id')
    exam_name = serializers.SerializerMethodField('get_exam_name')
    full_mark = serializers.SerializerMethodField('get_exam_full_mark')
    student_mark = serializers.SerializerMethodField('get_student_mark')
    is_started = serializers.SerializerMethodField('check_exam_is_started')
    exam_startdate = serializers.SerializerMethodField('get_exam_startdate')
    exam_duration = serializers.SerializerMethodField('get_exam_duration')

    def get_student_id(self, obj):
        user = User.objects.get(pk = obj.student.user.id)
        return user.id
    def get_student_name(self, obj):
        user = User.objects.get(pk = obj.student.user.id)
        return user.username
    def get_exam_name(self, obj):
        exam = Exam.objects.get(id = obj.exam.id)
        return exam.exam_name
    def get_exam_startdate(self, obj):
        exam = Exam.objects.get(id = obj.exam.id)
        return exam.exam_startdate
    def get_exam_duration(self, obj):
        exam = Exam.objects.get(id = obj.exam.id)
        return exam.exam_duration
    def get_exam_full_mark(self, obj):
        exam = Exam.objects.get(id = obj.exam.id)
        exam_questions = Question.objects.filter(exam = exam)
        total_mark = 0
        for question in exam_questions:
            total_mark += question.mark
        return total_mark
    def get_student_mark(self, obj):
        try:
            student_mark = ExamResults.objects.get(exam = obj.exam.id, student = obj.student.user.id).mark
            return student_mark
        except ExamResults.DoesNotExist:
            return 0
    def check_exam_is_started(self, obj):
        exam = Exam.objects.get(id = obj.exam.id)
        mins,hrs = math.modf(exam.exam_duration)
        exam_endtime = exam.exam_startdate + timedelta(hours = hrs, minutes=mins*60)
        if not timezone.now() >= exam.exam_startdate :
            return 'The Exam has not started yet'
        if not timezone.now() < exam_endtime:
            return 'The Exam is Closed'
        else:
            return 'The Exam is Open'



class StudentAllProgrammingTestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammingTestAllowedStudents
        fields = ('test_id','test_name','test_startdate','test_duration','student_id','student_name')
    student_name = serializers.SerializerMethodField('get_student_name')
    student_id = serializers.SerializerMethodField('get_student_id')
    test_name = serializers.SerializerMethodField('get_test_name')
    test_startdate = serializers.SerializerMethodField('get_test_startdate')
    test_duration = serializers.SerializerMethodField('get_test_duration')

    def get_student_id(self, obj):
        user = User.objects.get(pk = obj.student.user.id)
        return user.id
    def get_student_name(self, obj):
        user = User.objects.get(pk = obj.student.user.id)
        return user.username
    def get_test_name(self, obj):
        test = ProgrammingTest.objects.get(id = obj.test.id)
        return test.test_name
    def get_test_startdate(self, obj):
        test = ProgrammingTest.objects.get(id = obj.test.id)
        return test.test_startdate
    def get_test_duration(self, obj):
        test = ProgrammingTest.objects.get(id = obj.test.id)
        return test.test_duration

    def check_test_is_started(self, obj):
        test = ProgrammingTest.objects.get(id = obj.test.id)
        mins,hrs = math.modf(test.exam_duration)
        exam_endtime = test.exam_startdate + timedelta(hours = hrs, minutes=mins*60)
        if not timezone.now() >= test.exam_startdate :
            return 'The Exam has not started yet'
        if not timezone.now() < exam_endtime:
            return 'The Exam is Closed'
        else:
            return 'The Exam is Open'

class ExamResultSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ExamResults
        fields = ('id', 'student_name', 'mark')

    student_name = serializers.SerializerMethodField('get_student_name')
    id = serializers.SerializerMethodField('get_student_id')
    def get_student_name(self, obj):
        return obj.student.user.username
    def get_student_id(self, obj):
        return obj.student.user.id

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
        return obj.exam.exam_name

    def get_student_name(self, obj):
        return obj.student.user.username
    
    def get_question_text(self, obj):
        return obj.question.text

    def get_answer_text(self, obj):
        return obj.answer.text

    def is_answer_correct(self, obj):
        return obj.answer.is_correct


class StudentProgrammingAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProgrammingAnswer
        fields = ('student_name', 'student','test', 'test_name', 'question', 'question_text', 'answer', 'programming_language', 'output')

    test_name = serializers.SerializerMethodField('get_test_name')
    student_name = serializers.SerializerMethodField('get_student_name')
    question_text = serializers.SerializerMethodField('get_question_text')
    answer = serializers.SerializerMethodField('get_answer')
    output = serializers.SerializerMethodField('get_output')
    programming_language = serializers.SerializerMethodField('get_programming_language')


    def get_test_name(self, obj):
        return obj.test.test_name

    def get_student_name(self, obj):
        return obj.student.user.username

    def get_question_text(self, obj):
        return obj.question.text

    def get_answer(self, obj):
        return obj.answer

    def get_answer(self, obj):
        return obj.answer

    def get_programming_language(self, obj):
        return obj.programming_language

    def get_output(self, obj):
        return obj.output



class SupervisorDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamSupervisors
        fields = ('exam_id','exam_name','exam_startdate','exam_duration','is_started')
    exam_id = serializers.SerializerMethodField('get_exam_id')
    exam_name = serializers.SerializerMethodField('get_exam_name')
    is_started = serializers.SerializerMethodField('check_exam_is_started')
    exam_startdate = serializers.SerializerMethodField('get_exam_startdate')
    exam_duration = serializers.SerializerMethodField('get_exam_duration')

    def get_exam_id(self, obj):
        return obj
    def get_exam_name(self, obj):
        exam = Exam.objects.get(id = obj)
        return exam.exam_name
    def get_exam_startdate(self, obj):
        exam = Exam.objects.get(id = obj)
        return exam.exam_startdate
    def get_exam_duration(self, obj):
        exam = Exam.objects.get(id = obj)
        return exam.exam_duration
    def check_exam_is_started(self, obj):
        exam = Exam.objects.get(id = obj)
        mins,hrs = math.modf(exam.exam_duration)
        exam_endtime = exam.exam_startdate + timedelta(hours = hrs, minutes=mins*60)
        if not timezone.now() >= exam.exam_startdate :
            return 'The Exam has not started yet'
        if not timezone.now() < exam_endtime:
            return 'The Exam is Closed'
        else:
            return 'The Exam is Open'

class ReportViolationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Violation
        fields = '__all__'