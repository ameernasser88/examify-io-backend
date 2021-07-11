from typing import Callable
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.base import Model
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields.related import ForeignKey
from django.utils.timezone import now


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ("1", 'student'),
        ("2", 'examiner'),
        ("3", 'supervisor'),
    )
    user_type = models.CharField(choices=USER_TYPE_CHOICES,default="1",null=False , max_length=10)

    def __str__(self):
        return self.username


class Examiner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class Supervisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username

class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE,default=None, related_name='answer')
    text = models.TextField()
    is_correct = models.BooleanField(default=True)
    def __str__(self) -> str:
        qans = str(self.question)+str(self.text)
        return str(qans)
    
class Exam(models.Model):
    examiner = models.ForeignKey(Examiner,default=None, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=255, null=False,blank=False)
    exam_startdate = models.DateTimeField(null=False,blank=False)
    exam_duration = models.FloatField(null=False,blank=False)
    def __str__(self) -> str:
        return str(self.exam_name)

class Question(models.Model):
    exam = models.ForeignKey(Exam, default=None, on_delete=models.CASCADE)
    text = models.TextField()
    mark = models.FloatField(null = True)
    previous_question = models.ForeignKey("Question" , on_delete=models.CASCADE , null=True , blank=True)

    def __str__(self) -> str:
        return str(self.text)

class StudentAnswer(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "Student : " +str(self.student) + " Exam : " + str(self.exam) + "Question : " + str(self.question.text)+"Answer : " + str(self.answer.text)

class ExamResults(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    mark = models.FloatField()

    def __str__(self) -> str:
        return "Student : " +str(self.student) + " Exam : " + str(self.exam) + " Mark : " + str(self.mark)


class ExamSupervisors(models.Model):
    supervisor = models.ForeignKey(Supervisor,on_delete=models.SET_NULL,null = True, default=None)
    exam = ForeignKey(Exam, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.exam) +" "+ str(self.supervisor)

class AllowedStudents(models.Model):
    student = ForeignKey(Student, on_delete=models.CASCADE)
    exam = ForeignKey(Exam, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Supervisor,on_delete=models.SET_NULL,null = True, default=None)
    enter_time = models.DateTimeField(null= True, blank= True, default= None)
    submit_time = models.DateTimeField(null= True, blank= True, default= None)
    attendance = models.BooleanField(default= False)
    def __str__(self):
        return str(self.exam) + " " + str(self.student) + " "+ str(self.supervisor)


####### Programming ################

class ProgrammingTest(models.Model):
    examiner = models.ForeignKey(Examiner,default=None, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=255, null=False,blank=False)
    test_startdate = models.DateTimeField(null=False,blank=False)
    test_duration = models.FloatField(null=False,blank=False)
    def __str__(self) -> str:
        return str(self.test_name)


class ProgrammingQuestion(models.Model):
    test = models.ForeignKey(ProgrammingTest, default=None, on_delete=models.CASCADE)
    text = models.TextField()
    def __str__(self) -> str:
        return str(self.text)


class ProgrammingTestAllowedStudents(models.Model):
    student = ForeignKey(Student, on_delete=models.CASCADE)
    test = ForeignKey(ProgrammingTest, on_delete=models.CASCADE)
    enter_time = models.DateTimeField(null= True, blank= True, default= None)
    submit_time = models.DateTimeField(null= True, blank= True, default= None)

    def __str__(self):
        return str(self.student) + " " + str(self.test)


class StudentProgrammingAnswer(models.Model):
    programming_languages = (
        ("csharp", 'csharp'),
        ("python3", 'python3'),
        ("java", 'java'),
        ("php", 'php'),
        ("cpp14", 'cpp14'),
        ("go", 'go'),
    )
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    test = models.ForeignKey(ProgrammingTest, on_delete=models.CASCADE)
    question = models.ForeignKey(ProgrammingQuestion, on_delete=models.CASCADE)
    programming_language = models.CharField(choices=programming_languages,default="python3",null=False, max_length=100)
    answer = models.TextField()
    output = models.TextField(null=True)



class ErrorMessages(models.Model):
    error_message = models.TextField()
    def __str__(self):
        return str(self.error_message)


class Violation(models.Model):
    violation = models.TextField()
    time = models.DateTimeField(null= False, default=now)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)